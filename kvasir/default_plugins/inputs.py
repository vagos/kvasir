from kvasir.hooks import hookimpl
from kvasir.program import Property
from kvasir.utils import clean_llm_output, get_code_block, logger
import dspy

class Inputs(Property):
    """A list of input examples that exercise the component."""

    def to_lm(self):
        return ""

# TODO: use existing dspy config
lm = dspy.LM('openai/gpt-4o-mini')

@hookimpl
def apply(program):
    if "inputs" in program.annotations:
        return
    prompt = f"""You are analyzing a program.
    Your task is to generate a list of concrete inputs that would meaningfully exercise the behavior of the program.

Program:
{program.src}

Please return one input per line. Each input should be a value or an object suitable for a top-level function call.

Example:

```
val1, val2, val3
() => {{}}, val5, val6
```
"""
    output = "\n".join(lm(prompt))
    output = get_code_block(output)
    
    inputs = [line.strip() for line in output.splitlines() if line.strip()]

    program["inputs"] = Inputs("inputs", inputs)
    logger.debug(f"LLM-generated inputs: {inputs}")

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(inputs(p)).", "Program can be analyzed for representative inputs.")
