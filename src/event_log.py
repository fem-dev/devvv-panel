"""Small in-memory event log; never stores wallet or pool credentials."""
from __future__ import annotations

from datetime import datetime
from collections import deque


class EventLog:
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[str] = deque(maxlen=max_items)

    def add(self, message: str, level: str = "INFO") -> None:
        stamp = datetime.now().astimezone().strftime("%H:%M:%S")
        safe_message = str(message).replace("\n", " ")[:240]
        self._items.append(f"[{stamp}] [{level.upper()}] {safe_message}")

    def lines(self) -> list[str]:
        return list(self._items)
