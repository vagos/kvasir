from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("kvasir")
hookimpl = HookimplMarker("kvasir")


@hookspec
def apply(program):
    """
    Apply the plugin to the program.
    This can either extract a property from the program or modify it in some way.

    This should mutate or annotate the program object (e.g., program.signatures = ...).
    Returns set of extracted/modified properties.
    """


@hookspec
def verify(original_program, regenerated_program):
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
