"""Read-only host diagnostics. Values may be unavailable in restricted runtimes."""
from __future__ import annotations

import platform
import shutil
from pathlib import Path
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover - dependency is declared
    psutil = None


def _detect_linux_gpu_vendors() -> list[str]:
    """Read PCI vendor IDs from Linux sysfs; never runs external commands."""
    vendors: set[str] = set()
    drm_root = Path("/sys/class/drm")
    if not drm_root.exists():
        return []
    try:
        for device_file in drm_root.glob("card[0-9]*/device/vendor"):
            vendor_id = device_file.read_text(encoding="ascii").strip().lower()
            if vendor_id == "0x10de":
                vendors.add("NVIDIA")
            elif vendor_id in {"0x1002", "0x1022"}:
                vendors.add("AMD")
            elif vendor_id == "0x8086":
                vendors.add("Intel")
    except (OSError, UnicodeError):
        pass
    return sorted(vendors)


def detect_hardware() -> dict[str, Any]:
    info: dict[str, Any] = {
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine() or "نامشخص",
        "cpu": platform.processor() or "نامشخص",
        "logical_cores": None,
        "ram_gb": None,
        "gpu_vendors": _detect_linux_gpu_vendors() if platform.system() == "Linux" else [],
        "gpu_note": "تشخیص GPU در محیط‌های ابری/کانتینری یا سیستم‌عامل‌های غیرلینوکس ممکن است محدود باشد.",
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

    cpu_text = (info["cpu"] or "").upper()
    if "AMD" in cpu_text:
        info["cpu_vendor"] = "AMD"
    elif "INTEL" in cpu_text:
        info["cpu_vendor"] = "Intel"
    else:
        info["cpu_vendor"] = "نامشخص"
    return info
