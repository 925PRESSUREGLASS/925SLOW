import json
from click.testing import CliRunner

from backend.cli_runner import main


def test_cli_uses_router_agent():
    runner = CliRunner()
    result = runner.invoke(main, ["--prompt", "Clean 2 windows in Perth"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["quote_text"].startswith(">")
