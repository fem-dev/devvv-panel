"""Read-only host diagnostics. Values may be unavailable in restricted runtimes."""
from __future__ import annotations

import platform
import shutil
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover - dependency is declared
    psutil = None


def detect_hardware() -> dict[str, Any]:
    info: dict[str, Any] = {
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine() or "نامشخص",
        "cpu": platform.processor() or "نامشخص",
        "logical_cores": None,
        "ram_gb": None,
        "gpu_vendors": [],
        "gpu_note": "تشخیص GPU در محیط‌های ابری/کانتینری ممکن است محدود باشد.",
        "python": platform.python_version(),
        "disk_free_gb": None,
    }
    if psutil is not None:
        info["logical_cores"] = psutil.cpu_count(logical=True)
        try:
            info["ram_gb"] = round(psutil.virtual_memory().total / (1024**3), 1)
            info["disk_free_gb"] = round(shutil.disk_usage(".").free / (1024**3), 1)
        except OSError:
            pass

    # Read-only vendor hint; do not invoke vendor utilities or shell commands.
    cpu_text = (info["cpu"] or "").upper()
    if "AMD" in cpu_text:
        info["cpu_vendor"] = "AMD"
    elif "INTEL" in cpu_text:
        info["cpu_vendor"] = "Intel"
    else:
        info["cpu_vendor"] = "نامشخص"
    return info
