import logging

import click

from .plugins import load_plugins
from .program import Program
from .synth import regenerate
from .utils import logger
from .logic import KnowledgeBase, Query


@click.command()
@click.option("--input", "-i", required=True, help="Path to the source program")
@click.option("--query", "-q", required=True, help="Path to the transformation query")
@click.option(
    "--output", "-o", required=True, help="Path to the output regenerated program"
)
@click.option("--verbose", "-v", count=True, help="Increase verbosity of output")
def main(input, query, output, verbose):
    """Run a declarative program regeneration."""
    plugins = load_plugins()
    level = {
        0: logging.CRITICAL + 1,
        1: logging.INFO,
        2: logging.DEBUG,
    }.get(verbose, logging.DEBUG)
    logger.setLevel(level)

    program = Program(entry=input)
    query = Query(entry=query)
    kb = KnowledgeBase()
    logger.debug(f"Loaded program: {program}")

    program_ = regenerate(program, kb, query, plugins)

    print(f"Trasnformed\n\t{program}\ninto\n\t{program_}")

    program_.entry = output
    program_.save(output)
