from kvasir.program import Program
from kvasir.hooks import hookimpl

class JavaScriptProgram(Program):
    language = "javascript"

    def load(self):
        """Load the JavaScript code from the entry file."""
        with open(self.entry, 'r') as file:
            return file.read()

    def save(self, output):
        """Save the JavaScript code to the output file."""
        with open(output, 'w') as file:
            file.write(self.code)

@hookimpl
def language_support():
    return JavaScriptProgram
