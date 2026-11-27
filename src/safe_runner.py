"""Safety boundary for command preview.

There is deliberately no subprocess, shell, download, or miner-launch function.
"""
from __future__ import annotations


def execution_status() -> dict[str, str | bool]:
    return {
        "running": False,
        "mode": "preview-only",
        "message": "اجرای واقعی غیرفعال است؛ فقط پیش‌نمایش فرمان و تنظیمات نمایش داده می‌شود.",
    }
