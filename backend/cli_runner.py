"""CLI entry-point wrapping the Router/Agents for local usage."""

import json
import sys

import click


@click.command()
@click.option(
    "--prompt",
    "prompt_",
    required=True,
    help="Text to pass to RouterAgent",
)
def main(prompt_: str):  # noqa: D401,ANN001 – Click callback
    """Run a single prompt using RouterAgent."""

    from backend.agents.router_agent import RouterAgent

    result = RouterAgent.dispatch(prompt_)
    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
