import re

from kvasir.logic import KnowledgeBase
import kvasir.program
from kvasir.hooks import hookimpl
from kvasir.program import Property

class Signature(Property):
    """
    Represents a function signature extracted from a program.
    Contains the function name and its parameter list.
    """

@hookimpl
def precondition(program):
    return program["language"] == kvasir.program.Language.JS

@hookimpl
def apply(program):
    # Extract top-level function signatures using regex (simplified)
    pattern = r"function\s+(\w+)\s*\(([^)]*)\)"
    matches = re.findall(pattern, program.src)

    # Store as a list of (name, args)
    program["signature"] = Property("signature", [
        {"name": name, "args": [arg.strip() for arg in args.split(",") if arg.strip()]}
        for name, args in matches
    ]);

    return {"signature"}


@hookimpl
def verify(original_program, regenerated_program):
    orig_sigs: Property = original_program["signature"]
    regen_sigs: Property = regenerated_program["signature"]

    def normalize(sigs):
        return sorted((sig["name"], tuple(sig["args"])) for sig in sigs.value)

    return normalize(orig_sigs) == normalize(regen_sigs)

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(signature(p)).") 
