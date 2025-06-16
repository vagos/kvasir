from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Type

from .utils import logger


class Language(Enum):
    JS = "javascript"
    HS = "haskell"
    C = "c"

    def __str__(self):
        return self.value.capitalize()

    def suffix(self):
        """Return the file suffix for the language."""
        match self:
            case Language.JS:
                return ".js"
            case Language.HS:
                return ".hs"
            case Language.C:
                return ".c"
            case _:
                raise ValueError(f"Unsupported language: {self.value}")


def detect_language(entry) -> Language:
    """Detect the programming language based on the file extension."""
    if entry.endswith(".js"):
        return Language.JS
    elif entry.endswith(".hs"):
        return Language.HS
    elif entry.endswith(".c"):
        return Language.C
    else:
        raise ValueError(f"Unsupported file type: {entry}")

class Action(Enum):
    PRESERVE = "preserve"
    ELIMINATE = "eliminate"
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"

class Property():
    """Base class for properties that can be attached to programs."""
    def __init__(self, name: str, value: Any, action: Action = Action.PRESERVE):
        self.name = name
        self.value = value
        self.action = action

    def to_lm(self) -> str:
        """Convert the property to a string representation for a language model. This should include domain-specific information."""
        return f"""The program has the property '{self.name}'.
It is {self.value}.
It should be {self.action.value}d during regeneration.\n
"""

    def set_action(self, action: Action):
        """Set the action to be taken on this property. This is done by the planner."""
        self.action = action

    def __lt__(self, other: "Property") -> bool:
        """Compare properties based on their value."""
        return self.value < other.value

    def __gt__(self, other: "Property") -> bool:
        """Compare properties based on their value."""
        return self.value > other.value

    def __repr__(self):
        return f"{self.name}: {self.value}"

class ProgramMeta(type):
    registry: dict[Language, Type["Program"]] = {}

    def __call__(cls, entry, *args, **kwargs):
        lang = detect_language(entry)
        subclass = cls.registry.get(lang, cls)
        logger.debug(
            f"Detected language: {lang}, using subclass: {subclass.__name__}"
        )
        return super(ProgramMeta, subclass).__call__(entry, *args, **kwargs)


@dataclass
class Program(metaclass=ProgramMeta):
    language: Language # Set by subclasses
    annotations: dict[str, Property] # For plugins to store data
    entry: Path
    src: str

    def __init__(self, entry):
        self.entry = Path(entry)
        self.annotations = {}
        self.src = self.load()
        assert self.src, f"Failed to load program source from {self.entry}"

    def to_lm(self) -> str:
        """Convert the program to a string representation for a language model."""
        repr = ""
        repr += f"The program is written in {self.language}.\n"
        for _name, prop in self.annotations.items():
            repr += prop.to_lm()

        return repr

    def to_logic(self) -> str:
        """Convert the program to a logic representation."""
        return f"language(p, {self.language.value})."

    def load(self) -> str:
        logger.debug(f"Loading program from {self.entry}")
        """Load the program src from the entry file."""
        with open(self.entry, "r") as file:
            return file.read().strip()

    def save(self, output):
        """Save the program src to the output file."""
        with open(output, "w") as file:
            file.write(self.src)

    def __setitem__(self, key, value):
        self.annotations[key] = value

    def __getitem__(self, key) -> Property:
        return self.annotations[key]


# Language-specific programs
class JavaScriptProgram(Program):
    language = Language.JS

class HaskellProgram(Program):
    language = Language.HS

class CProgram(Program):
    language = Language.C

# Register the language-specific programs
ProgramMeta.registry[Language.JS] = JavaScriptProgram
ProgramMeta.registry[Language.HS] = HaskellProgram
ProgramMeta.registry[Language.C] = CProgram
