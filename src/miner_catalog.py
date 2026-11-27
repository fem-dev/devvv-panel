"""Curated, informational miner catalog and compatibility hints.

No binary downloads or process execution are implemented in this project.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Miner:
    name: str
    algorithms: tuple[str, ...]
    hardware: tuple[str, ...]
    platforms: tuple[str, ...]
    description: str
    official_url: str
    notes: str


MINERS: tuple[Miner, ...] = (
    Miner(
        name="XMRig",
        algorithms=("RandomX", "KawPow", "CryptoNight (legacy)"),
        hardware=("CPU", "AMD GPU", "NVIDIA GPU"),
        platforms=("Windows", "Linux", "macOS"),
        description="نرم‌افزار متن‌باز با تمرکز اصلی بر استخراج RandomX و پردازنده.",
        official_url="https://github.com/xmrig/xmrig",
        notes="برای RandomX معمولاً CPU و حافظهٔ مناسب اهمیت زیادی دارند؛ نسخه و الگوریتم را بررسی کنید.",
    ),
    Miner(
        name="SRBMiner-MULTI",
        algorithms=("RandomX", "KawPow", "Autolykos", "Etchash"),
        hardware=("CPU", "AMD GPU", "NVIDIA GPU"),
        platforms=("Windows", "Linux"),
        description="گزینه‌ای چندمنظوره؛ پشتیبانی دقیق به نسخه و سخت‌افزار وابسته است.",
        official_url="https://github.com/doktor83/SRBMiner-Multi",
        notes="پیش از انتخاب، فهرست الگوریتم‌های نسخهٔ فعلی و محدودیت‌های درایور را بررسی کنید.",
    ),
    Miner(
        name="lolMiner",
        algorithms=("Autolykos", "Etchash", "Beam", "Equihash"),
        hardware=("AMD GPU", "NVIDIA GPU"),
        platforms=("Windows", "Linux"),
        description="ماینر GPU با پشتیبانی الگوریتمی وابسته به نسخه.",
        official_url="https://github.com/Lolliedieb/lolMiner-releases",
        notes="سازگاری GPU، نسخهٔ درایور و وضعیت نگه‌داری پروژه را پیش از استفاده بررسی کنید.",
    ),
    Miner(
        name="BzMiner",
        algorithms=("Etchash", "KawPow", "Autolykos", "NexaPow"),
        hardware=("AMD GPU", "NVIDIA GPU"),
        platforms=("Windows", "Linux"),
        description="ماینر چندالگوریتمی GPU؛ قابلیت‌ها در انتشارهای مختلف تغییر می‌کنند.",
        official_url="https://github.com/bzminer/bzminer",
        notes="فقط از منبع رسمی دریافت کنید و checksum/امضای انتشار را بررسی کنید.",
    ),
)


def recommend_miners(gpu_vendors: tuple[str, ...], has_cpu: bool = True) -> list[Miner]:
    """Return miners with a hardware class matching the detected host."""
    available = {"CPU"} if has_cpu else set()
    for vendor in gpu_vendors:
        if vendor == "NVIDIA":
            available.add("NVIDIA GPU")
        elif vendor == "AMD":
            available.add("AMD GPU")
    return [miner for miner in MINERS if available.intersection(miner.hardware)]


def get_miner(name: str) -> Miner | None:
    return next((miner for miner in MINERS if miner.name == name), None)
