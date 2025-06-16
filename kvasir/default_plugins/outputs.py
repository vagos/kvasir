import subprocess
import json

from kvasir.hooks import hookimpl
from kvasir.program import Property
from kvasir.utils import logger
from kvasir.program import Language

class IOExamples(Property):
    """A list of (input, output) pairs derived from executing the program."""

    def to_lm(self):
        return ""

@hookimpl
def apply(program):
    if "inputs" not in program.annotations:
        logger.warning("No inputs found; skipping output generation.")
        return

    inputs = program["inputs"].value
    outputs = []

    match program.language:
        case Language.JS:
            outputs = run_nodejs(program.src, inputs)
        case Language.HS:
            outputs = run_haskell(program.src, inputs)
        case Language.C:
            outputs = run_c(program.src, inputs)
        case _:
            raise ValueError(f"Unsupported language: {program.language}")

    program["outputs"] = IOExamples("outputs", outputs)
    logger.debug(f"Generated I/O examples: {outputs}")

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(outputs(p)).", "Program can be executed to observe outputs.")

@hookimpl
def verify(original_program, regenerated_program):
    """Verify that the outputs of the program match the expected outputs."""
    assert "outputs" in original_program.annotations\
    and "outputs" in regenerated_program.annotations, "Both programs must have outputs."

    outputs = original_program["outputs"].value
    outputs_ = regenerated_program["outputs"].value

    assert len(outputs) == len(outputs_), "Output lengths do not match."

    for (input, output), (_, output_) in zip(outputs, outputs_):
        if output != output_:
            logger.error(f"Output mismatch for input {input}: {output} != {output_}")
            return False

    logger.info("All outputs match.")
    return True

# Language-specific runners

def run_nodejs(js_src, inputs):
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w") as f:
        f.write(f"module.exports = {js_src}\n")
        f.write("const main = typeof module !== 'undefined' && module.exports;\n")
        f.write("if (main) globalThis.__main = module.exports;\n")
        path = f.name
        logger.debug(f"Wrote JavaScript source to temporary file {path}")

    results = []
    for i in inputs:
        try:
            result = subprocess.check_output(
                ["node", "-e", f"""
                const m = require('{path}');
                const r = m({i});
                console.log(r);
                """],
                stderr=subprocess.DEVNULL,
                timeout=2
            )

            logger.debug(f"Node.js output for input {i}: '{result.decode()}'")
            parsed = result.decode()
        except Exception as e:
            logger.error(f"Error running Node.js for input {i}: {e}")
            parsed = None
        results.append((i, parsed))
    return results

def run_haskell(src, inputs):
    # Placeholder: invoke GHCi, parse results, etc.
    return [(i, f"output-for-{i}") for i in inputs]

def run_c(src, inputs):
    # Placeholder: compile with gcc, run with input via stdin or argv
    return [(i, f"output-for-{i}") for i in inputs]
