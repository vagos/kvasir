from kvasir.hooks import hookimpl
from kvasir.program import Property


class ProgramLength(Property):
    """
    Represents the length of a program's source code.
    This property can be used to analyze or manipulate the program based on its length.
    """

@hookimpl
def apply(program):
    program["len"] = ProgramLength("len", program.src.count("\n") + 1)

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(len(p)).", "This program can have its length calculated.")
