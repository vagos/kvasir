import logging

import dotenv
import dspy
import tempfile

import kvasir.logic as logic
from kvasir.program import Program

from .utils import logger

dotenv.load_dotenv()

lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)

class RegenerateProgram(dspy.Signature):
    """LLM signature for program regeneration."""
    input_program: str  = dspy.InputField(desc="Input program to be regenerated.")
    output_program: str = dspy.OutputField(desc="Source code of the regenerated program.")

class SynthesizeProgram(dspy.Module):
    def __init__(self):
        self.synthesize = dspy.ChainOfThought(RegenerateProgram)

    def forward(self, program: Program) -> Program:
        """Regenerate the program's source code based on the context provided."""
        regenerated_program_src = self.synthesize(input_program=program.to_lm()).output_program

        with tempfile.NamedTemporaryFile(delete=False, suffix=program.language.suffix()) as temp_file:
            temp_file.write(regenerated_program_src.encode('utf-8'))
            temp_file_path = temp_file.name
            regenerated_program = Program(entry=temp_file_path)
            regenerated_program.annotations = program.annotations.copy() # TODO: Do this better
            return regenerated_program

def regenerate(program, kb, query, plugins) -> Program:
    for plugin in plugins:
        if hasattr(plugin, "extract"):
            logger.info(f"Extracting properties with {plugin.__name__}")
            plugin.extract(program)

        if hasattr(plugin, "knowledge"):
            logger.info(f"Adding knowledge with {plugin.__name__}")
            plugin.knowledge(kb, program)

    plan = logic.plan(kb, query, program)
    program_ = synthesize(program, plan)

    for plugin in plugins:
        logger.info(f"Verifying {program_} against {program} with {plugin.__name__}")

        if hasattr(plugin, "verify"):
            plugin.verify(program, program_)

    return program_


def synthesize(program, plan) -> Program:
    """Synthesize a new program based on the plan."""

    logger.info(f"Synthesizing program with plan: {plan}")
    synthesize = SynthesizeProgram()
    regenerated_program = synthesize(program)
    if logger.level == logging.DEBUG:
        dspy.inspect_history(10)
    
    return regenerated_program
