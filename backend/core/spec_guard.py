"""Minimal SpecGuard so tests can assert a pass/fail score."""

from dataclasses import dataclass


@dataclass
class SpecResult:
    score: float
    violations: list[str]


def grade(response: str) -> SpecResult:  # noqa: D401,ANN001
    """Very relaxed grader – 1.0 if response starts with ">", else 0.0."""

    if response.lstrip().startswith(">"):
        return SpecResult(score=1.0, violations=[])
    return SpecResult(score=0.0, violations=["missing blockquote"])
