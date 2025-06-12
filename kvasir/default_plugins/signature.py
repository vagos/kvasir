import re

import kvasir.program
from kvasir.hooks import hookimpl
from kvasir.program import Property


class Signature(Property):
    """
    Represents a function signature extracted from a program.
    Contains the function name and its parameter list.
    """

def extract_js(src: str) -> list: 
    """
    Extract JavaScript function signatures from the source code.
    """
    # For simplicity, let's assume we extract functions in the form of:
    # function name(arg1, arg2) { ... }
    pattern = r"function\s+(\w+)\s*\(([^)]*)\)"
    matches = re.findall(pattern, src)
    return [{"name": name, "args": [arg.strip() for arg in args.split(",") if arg.strip()]} for name, args in matches]

def extract_hs(src: str) -> list:
    """
    Extract Haskell function signatures from the source code.
    """
    # Look for lines like "name :: type1 -> type2 -> …"
    pattern = r"^(\w+)\s*::\s*(.+)$"
    matches = re.findall(pattern, src, re.MULTILINE)

    # For each signature, split the RHS on '->' to get a list of type args
    result = []
    for name, type_sig in matches:
        args = [arg.strip() for arg in type_sig.split("->") if arg.strip()]
        result.append({"name": name, "args": args})
    return result

def extract_c(src: str) -> list:
    """
    Extract C function signatures (both declarations and definitions)
    from the source code.
    Returns a list of dicts with keys: name, return_type, args.
    """
    # Match:
    #   <return-type> <funcname>(<arg-list>) ;
    # or
    #   <return-type> <funcname>(<arg-list>) {
    pattern = r"""
      ([_a-zA-Z]\w*(?:\s+[\w\*\_]+)*)   # return type (e.g. "float", "const char *")
      \s+
      ([_a-zA-Z]\w*)                    # function name
      \s*
      \(
        ([^)]*)                         # argument list (anything but ')')
      \)
      \s*
      (?:;|\{)                          # then either a ; (declaration) or { (definition)
    """
    matches = re.findall(pattern, src, re.VERBOSE|re.MULTILINE)

    functions = []
    for return_type, name, args in matches:
        arg_list = [arg.strip() for arg in args.split(",") if arg.strip()]
        functions.append({
            "return_type": return_type.strip(),
            "name": name,
            "args": arg_list
        })
    return functions

@hookimpl
def apply(program):
    # Extract top-level function signatures using regex (simplified)
    # Store as a list of (name, args)

    match program.language:
        case kvasir.program.Language.JS:
            signatures_value = extract_js(program.src)
        case kvasir.program.Language.HS:
            signatures_value = extract_hs(program.src)
        case kvasir.program.Language.C:
            signatures_value = extract_c(program.src)
        case _:
            raise ValueError(f"Unsupported language: {program.language}")
    program["signature"] = Property("signature", signatures_value)

@hookimpl
def verify(original_program, regenerated_program):
    orig_sigs: Property = original_program["signature"]
    regen_sigs: Property = regenerated_program["signature"]

    def normalize(sigs):
        # return sorted((sig["name"], tuple(sig["args"])) for sig in sigs.value)
        return sorted((sig["name"] for sig in sigs.value))

    return normalize(orig_sigs) == normalize(regen_sigs)

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(signature(p)).") 
