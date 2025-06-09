import logging

import dotenv
import dspy
import tempfile

import kvasir.logic as logic
from kvasir.logic import Query
from kvasir.program import Program

from .utils import logger, clean_llm_output

dotenv.load_dotenv()

lm = dspy.LM('openai/gpt-4o-mini')
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
            logger.info(f"Writing regenerated program to {file.name}")
            file.write(regenerated_program_src)
            file_path = file.name
        regenerated_program = Program(entry=file_path)
        regenerated_program.annotations = program.annotations.copy() # TODO: Do this better
        return regenerated_program

def regenerate(program, kb, query, plugins) -> Program:
    kb.add_logic(program.to_logic())
    for plugin in plugins:
        if hasattr(plugin, "knowledge"):
            logger.info(f"Adding knowledge with {plugin.__name__}")
            plugin.knowledge(kb, program)

    plan = logic.plan(kb, query, program)
    logger.info(f"Generated plan: {plan}")

    for plugin in plugins:
        logger.info(f"Trying to apply {plugin.__name__} to the program {program}")
        if hasattr(plugin, "apply") and plan.does(plugin.__name__):
            logger.info(f"Applying {plugin.__name__}")
            plugin.apply(program)

    program_ = synthesize(program, plan)

    for plugin in plugins:
        if hasattr(plugin, "verify") and plan.does(plugin.__name__):
            logger.info(f"Verifying {program_} against {program} with {plugin.__name__}")
            plugin.verify(program, program_)

    return program_


def synthesize(program, plan) -> Program:
    """Synthesize a new program based on the plan."""

    logger.info(f"Synthesizing program with plan: {plan}")
    synthesize = SynthesizeProgram()
    regenerated_program = synthesize(program)
    if logger.level == logging.DEBUG:
        dspy.inspect_history()
    
    return regenerated_program
