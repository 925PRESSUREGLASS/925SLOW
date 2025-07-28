# SPDX-License-Identifier: MIT
"""Centralised JSON logger (tiny – will be expanded with file/telemetry sinks)."""

import json
import sys
from datetime import datetime, timezone


def log(event: str, **payload):  # noqa: D401,ANN001 – generic helper
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **payload,
    }
    sys.stdout.write(json.dumps(record) + "\n")

