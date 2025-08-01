"""Core utilities (LLM provider, prompt manager, SpecGuard stub)."""

from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"


def load_config() -> dict:  # noqa: ANN001 – simple helper
    if CONFIG_PATH.exists():
        return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    return {}
