"""CLI entry\u2011point wrapping the Router/Agents for local usage."""

import json
import sys
from pathlib import Path

import click

from backend.api.root import healthcheck  # quick sanity check


@click.command()
@click.option("--prompt", "prompt_", required=True, help="Text to pass to QuoteAgent")
def main(prompt_: str):  # noqa: D401,ANN001 \u2013 Click callback
    """Run a single quote in offline mode (stub for now)."""

    from backend.agents import QuoteAgent

    result = QuoteAgent().run(prompt_)
    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())

