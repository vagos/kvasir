from kvasir.hooks import hookimpl
from kvasir.program import Program, Language
from dataclasses import dataclass


class JavaScriptProgram(Program):
    language = Language.JS

    def load(self):
        """Load the JavaScript code from the entry file."""
        with open(self.entry, "r") as file:
            return file.read()

    def save(self, output):
        """Save the JavaScript code to the output file."""
        with open(output, "w") as file:
            file.write(self.src)


@hookimpl
def language_support():
    return JavaScriptProgram
