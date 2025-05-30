import kvasir.program

from kvasir.hooks import hookimpl
import re

@hookimpl
def precondition(program):
    return program["language"] == kvasir.program.Language.JS

@hookimpl
def extract(program):
    # Extract top-level function signatures using regex (simplified)
    pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
    matches = re.findall(pattern, program.code)

    # Store as a list of (name, args)
    program.signatures = [
        {"name": name, "args": [arg.strip() for arg in args.split(",") if arg.strip()]}
        for name, args in matches
    ]

    return { "signatures" }

@hookimpl
def verify(o_p, r_p):
    orig_sigs = o_p.signatures
    regen_sigs = r_p.signatures

    def normalize(sigs):
        return sorted((sig["name"], tuple(sig["args"])) for sig in sigs)

    return normalize(orig_sigs) == normalize(regen_sigs)
