from dataclasses import dataclass


@dataclass(slots=True)
class WindowJob:
    """Simple per-pane pricing with a bulk discount."""

    panes: int

    def price(self) -> float:
        base_rate = 10.0
        if self.panes > 15:
            base_rate *= 0.9  # 10% discount for volume
        return self.panes * base_rate
