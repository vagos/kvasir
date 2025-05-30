import kvasir.logic as logic
from kvasir.program import Program

from .utils import logger


def transform(program, query, plugins) -> Program:
    for plugin in plugins:
        if hasattr(plugin, "extract"):
            logger.info(f"Extracting properties with {plugin.__name__}")
            plugin.extract(program)

    plan = logic.plan(query, program)

    program_ = synthesize(program, plan)

    for plugin in plugins:
        if hasattr(plugin, "verify"):
            plugin.verify(program, program_)

    return program_


def synthesize(program, plan):
    return program
