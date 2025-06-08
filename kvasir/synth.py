import logging

import dotenv
import dspy

import kvasir.logic as logic
from kvasir.program import Program

from .utils import logger

dotenv.load_dotenv()

lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)

class RegenerateProgram(dspy.Signature):
    """LLM signature for program regeneration."""
    input_program: Program  = dspy.InputField(desc="Input program to be regenerated.")
    output_program: Program = dspy.OutputField(desc="Regenerated program based on the context provided.")

class SynthesizeProgram(dspy.Module):
    def __init__(self):
        self.synthesize = dspy.ChainOfThought(RegenerateProgram)

    def forward(self, program: Program) -> dspy.Prediction:
        """Regenerate the program's source code based on the context provided."""
        regenerated_program = self.synthesize(input_program=program).output_program
        return dspy.Prediction(output_program=regenerated_program)

def transform(program, kb, query, plugins) -> Program:
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
    prediction = synthesize(program)

    regenerated_program = prediction.output_program
    if logger.level == logging.DEBUG:
        dspy.inspect_history(10)
    
    return regenerated_program
