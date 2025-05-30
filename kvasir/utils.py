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

# Disable by default
logger.setLevel(logging.CRITICAL + 1)
