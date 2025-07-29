import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_runs(tmp_path: Path):
    env = os.environ.copy()
    env["DATA_DIR"] = str(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.cli_runner",
            "--prompt",
            "Clean 2 windows in Perth",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    data = json.loads(result.stdout)
    assert "$20.00" in data["quote_text"]
