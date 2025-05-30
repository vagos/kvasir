import click
from kvasir.program import Program
from kvasir.synth import transform
from kvasir.plugins import load_plugins
from kvasir.query import Query


@click.command()
@click.option("--input", "-i", required=True, help="Path to the source program")
@click.option("--query", "-q", required=True, help="Path to the transformation query")
@click.option("--output", "-o", required=True, help="Path to the output regenerated program")
def main(input, query, output):
    """Run a declarative program regeneration."""
    program = Program(entry=input)
    query = Query(entry=query)
    plugins = load_plugins()

    program_ = transform(program, query, plugins)

    program_.save(output)
