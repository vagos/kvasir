from kvasir.hooks import hookimpl
from kvasir.program import Property

class ProgramLength(Property):
    """
    Represents the length of a program's source code.
    This property can be used to analyze or manipulate the program based on its length.
    """

    def __lt__(self, other):
        return self.value < other.value

@hookimpl
def apply(program):
    program["len"] = ProgramLength("len", len(program.src))

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(len(p)).", "This program can have its length calculated.")
