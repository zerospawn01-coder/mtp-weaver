from __future__ import annotations


class _LogicalClock:
    def __init__(self) -> None:
        self.value = 0

    def tick(self) -> int:
        self.value += 1
        return self.value


def get_clock() -> _LogicalClock:
    return _LogicalClock()

