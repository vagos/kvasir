import logging
import sys

logger = logging.getLogger("kvasir")

# Remove all existing handlers
if logger.hasHandlers():
    logger.handlers.clear()

# Attach handler with formatter
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(levelname)-4s | %(filename)s:%(lineno)d - %(message)s", datefmt="%H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def clean_llm_output(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].lstrip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

def get_code_block(text: str) -> str:
    """
    Extract the first code block from a text string.
    A code block is defined as text between triple backticks (```).
    """
    lines = text.splitlines()
    in_code_block = False
    code_lines = []

    for line in lines:
        if line.strip() == "```":
            if in_code_block:
                break  # End of code block
            else:
                in_code_block = True  # Start of code block
                continue

        if in_code_block:
            code_lines.append(line)

    return "\n".join(code_lines).strip()

def plugin_basename(name: str) -> str:
    """
    Extract the base name of a plugin from its full name.
    This is used to identify the plugin without its module path.
    """
    return name.split('.')[-1] if '.' in name else name

# Disable by default
logger.setLevel(logging.CRITICAL + 1)
