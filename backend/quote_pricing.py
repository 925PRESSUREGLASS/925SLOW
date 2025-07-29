from dataclasses import dataclass


@dataclass(slots=True)
class WindowJob:
    panes: int

    def price(self) -> float:
        """Return job price using volume-based discount."""
        base = 10.0
        if self.panes > 15:
            base *= 0.9
        return self.panes * base
