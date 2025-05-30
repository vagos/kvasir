import kvasir.logic as logic
from kvasir.program import Program


def transform(program, query, plugins) -> Program:
    for plugin in plugins:
        if hasattr(plugin, "extract"):
            plugin.extract(program)

    plan = logic.plan(query, program)

    program_ = synthesize(program, plan)

    for plugin in plugins:
        if hasattr(plugin, "verify"):
            plugin.verify(program, program_)

    return program_

def synthesize(program, plan):
    return program
