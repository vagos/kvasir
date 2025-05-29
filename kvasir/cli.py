import click
from sysregen.runner import run_sysregen
from sysregen.config import load_plugins, Config

@click.command()
@click.option("--input", "-i", required=True, help="Path to the source program")
@click.option("--query", "-q", required=True, help="Path to the transformation query")
@click.option("--output", "-o", required=True, help="Path to the output regenerated program")
@click.option("--plugin", "-p", multiple=True, help="Additional plugin module paths")
def main(input, query, output, plugin):
    """Run a declarative program regeneration."""
    config = Config(plugin_paths=plugin)
    load_plugins(config)
    run_sysregen(input_path=input, query_path=query, output_path=output, config=config)
