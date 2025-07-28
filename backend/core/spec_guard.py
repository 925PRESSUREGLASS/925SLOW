# SPDX-License-Identifier: MIT
"""Lightweight markdown rule checker for QuoteAgent outputs."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_ATTR_RE = re.compile(r"^>\s+—\s+QuoteGPT,\s+\d{4}")
_CURRENCY_RE = re.compile(r"\$\d{1,3}(?:,?\d{3})*(?:\.\d{2})?")


@dataclass(slots=True)
class SpecResult:
    score: float
    violations: list[str] = field(default_factory=list)


def grade(response_md: str) -> SpecResult:  # noqa: D401,ANN001
    """Return a compliance score (0‑1) and violation list for **specs/quote_generation.md**."""

    lines = [l.rstrip() for l in response_md.strip().splitlines() if l.strip()]
    if not lines:
        return SpecResult(0.0, ["empty response"])

    score, violations = 1.0, []

    # Q‑1 – blockquote start
    if not lines[0].startswith(">"):
        score -= 0.2
        violations.append("missing blockquote (Q‑1)")

    # Q‑2 – currency
    if not _CURRENCY_RE.search(lines[0]):
        score -= 0.2
        violations.append("no currency value (Q‑2)")

    # Q‑3 – suburb heuristic
    if " in " in lines[0].lower():
        after_in = lines[0].split(" in ")[-1]
        if not re.search(r"[A-Z][a-z]+", after_in):
            score -= 0.1
            violations.append("missing suburb (Q‑3)")
    else:
        score -= 0.1
        violations.append("missing suburb (Q‑3)")

    # Q‑4 – attribution line
    if len(lines) < 2 or not _ATTR_RE.match(lines[1]):
        score -= 0.3
        violations.append("invalid attribution (Q‑4)")

    # Q‑5 – rationale length ≤ 2 sentences
    body = " ".join(lines[2:]) if len(lines) > 2 else ""
    sentences = re.split(r"[.!?]+\s+", body.strip())
    if not body:
        score -= 0.2
        violations.append("missing rationale (Q‑5)")
    elif len(sentences) > 2:
        score -= 0.1
        violations.append("rationale too long (Q‑5)")

    return SpecResult(max(score, 0.0), violations)
