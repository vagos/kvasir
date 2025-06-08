import logging

import click

from .plugins import load_plugins
from .program import Program
from .query import Query
from .synth import transform
from .utils import logger
from .logic import KnowledgeBase


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

    logger.info(f"Loaded program: {program}")

    program_ = transform(program, kb, query, plugins)
    logger.info(f"Tranformed program {program} to {program_}")

    program_.save(output)
