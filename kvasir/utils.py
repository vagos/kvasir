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

# Disable by default
logger.setLevel(logging.CRITICAL + 1)
