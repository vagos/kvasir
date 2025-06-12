import logging
import copy

import dotenv
import dspy
import tempfile

import kvasir.logic as logic
from kvasir.logic import Query
from kvasir.program import Program, Action

from .utils import logger, clean_llm_output
from kvasir import utils

dotenv.load_dotenv()

lm = dspy.LM('openai/gpt-4o-mini')
local_lm = dspy.LM('ollama_chat/codellama:7b', api_base='http://localhost:11434', api_key='')
dspy.configure(lm=lm)

class RegenerateProgram(dspy.Signature):
    """
    You should synthesize the program's source code while preserving the properties that are marked as to be preserved.
    """
    input_program: str  = dspy.InputField(desc="Input program to be regenerated.")
    output_program: str = dspy.OutputField(desc="Source code of the regenerated program.")

class SynthesizeProgram(dspy.Module):
    def __init__(self):
        self.synthesize = dspy.ChainOfThought(RegenerateProgram)

    def forward(self, program: Program) -> Program:
        """Regenerate the program's source code based on the context provided."""
        regenerated_program_src = self.synthesize(input_program=program.to_lm()).output_program
        regenerated_program_src = clean_llm_output(regenerated_program_src)
        logger.debug(f"Regenerated program source code: {regenerated_program_src}")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=program.language.suffix()) as file:
            logger.debug(f"Writing regenerated program to {file.name}")
            file.write(regenerated_program_src)
            file_path = file.name
        regenerated_program = Program(entry=file_path)
        return regenerated_program

def regenerate(program, kb, query, plugins) -> Program:
    logger.debug(f"Plugins loaded: {[plugin.__name__ for plugin in plugins]}")

    program = copy.deepcopy(program)

    kb.add_logic(program.to_logic())
    for plugin in plugins:
        if hasattr(plugin, "knowledge"):
            logger.debug(f"Adding knowledge with {plugin.__name__}")
            plugin.knowledge(kb, program)

    plan = logic.plan(kb, query, program)
    logger.info(f"Generated plan: {plan}")

    used_plugins = { utils.plugin_basename(plugin.__name__): plugin for plugin in plugins if plan.does(plugin.__name__) }

    program_ = program

    while not plan.is_fullfilled():
        for plugin in used_plugins.values():
            if hasattr(plugin, "apply"):
                logger.debug(f"Applying {plugin.__name__}")
                plugin.apply(program)

        for plugin in used_plugins.values():
            if hasattr(plugin, "transform"):
                logger.debug(f"Transforming program with {plugin.__name__}")
                plugin.transform(program)

        for property, action in plan.properties.items():
            program[property].set_action(action)

        program_ = synthesize(program, plan)

        for plugin in used_plugins.values():
            if hasattr(plugin, "apply"):
                logger.debug(f"Applying {plugin.__name__}")
                plugin.apply(program_)

        for property, action in plan.properties.items():
            plugin = used_plugins[property]
            match action:
                case Action.PRESERVE:
                    if hasattr(plugin, "verify"):
                        logger.debug(f"Preserving property {property} with {plugin.__name__}")
                        ok = plugin.verify(program, program_)
                        logger.debug(f"Property {property} preserved: {ok}")
                case Action.ELIMINATE:
                    if hasattr(plugin, "verify"):
                        logger.debug(f"Eliminating property {property} with {plugin.__name__}")
                        ok = not plugin.verify(program, program_)
                        logger.debug(f"Property {property} eliminated: {ok}")
                case Action.MAXIMIZE:
                    ok = program_[property] > program[property]
                    logger.debug(f"Maximizing property {property}: {ok}")
                case Action.MINIMIZE:
                    ok = program_[property] < program[property]
                    logger.debug(f"Minimizing property {property}: {ok}")

        program, program_ = program_, program
        break

    return program


def synthesize(program, plan) -> Program:
    """Synthesize a new program based on the plan."""
    synthesize = SynthesizeProgram()
    regenerated_program = synthesize(program)
    if logger.level == logging.DEBUG:
        dspy.inspect_history()
    
    return regenerated_program
