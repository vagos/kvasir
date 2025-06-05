from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("kvasir")
hookimpl = HookimplMarker("kvasir")


@hookspec
def extract(program):
    """
    Extract a property from the program.

    Should mutate or annotate the program object (e.g., program.signatures = ...).
    Returns set of extracted properties
    """


@hookspec
def verify(o_p, r_p):
    """
    Verify that a property holds between the original and regenerated program.

    Return True if valid, False otherwise.
    """


@hookspec
def knowledge(kb, program):
    """
    Add domain-specific rules or constraints to the logic engine's knowledge base.

    Accepts a KnowledgeBase object and may mutate it (e.g., kb.add_rule(...)).
    """


@hookspec
def language_support():
    """
    Return the program subclass that this plugin supports.
    """
