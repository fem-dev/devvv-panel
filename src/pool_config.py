"""Pool form validation and safe command preview generation."""
from __future__ import annotations

import re
import shlex
from dataclasses import dataclass

_HOST_RE = re.compile(r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*$")
_WALLET_RE = re.compile(r"^[A-Za-z0-9:_-]{8,160}$")
_WORKER_RE = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")


@dataclass(frozen=True)
class PoolConfig:
    host: str
    port: int
    wallet: str
    worker: str = "worker01"
    password: str = "x"
    algorithm: str = "RandomX"


def validate_pool_config(config: PoolConfig) -> list[str]:
    errors: list[str] = []
    host = config.host.strip()
    if not _HOST_RE.fullmatch(host):
        errors.append("آدرس استخر معتبر نیست؛ فقط نام دامنه یا IP بدون پروتکل وارد کنید.")
    if not 1 <= int(config.port) <= 65535:
        errors.append("پورت باید بین 1 تا 65535 باشد.")
    if not _WALLET_RE.fullmatch(config.wallet.strip()):
        errors.append("شناسه کیف پول باید 8 تا 160 نویسه و فقط شامل حروف، عدد یا : _ - باشد.")
    if not _WORKER_RE.fullmatch(config.worker.strip()):
        errors.append("نام Worker فقط می‌تواند شامل حروف، عدد، نقطه، خط تیره و زیرخط باشد.")
    if len(config.password) > 64 or any(ch in config.password for ch in "\r\n"):
        errors.append("رمز استخر بیش از حد طولانی یا نامعتبر است.")
    if not config.algorithm.strip():
        errors.append("الگوریتم را انتخاب کنید.")
    return errors


def build_preview(config: PoolConfig, miner_name: str) -> str:
    """Build a human-readable example; intentionally never executes it."""
    args = [
        f"./{miner_name.lower()}",
        "--url", f"{config.host.strip()}:{int(config.port)}",
        "--user", config.wallet.strip(),
        "--pass", config.password,
        "--worker", config.worker.strip(),
        "--algo", config.algorithm,
    ]
    return " ".join(shlex.quote(part) for part in args) + "  # پیش‌نمایش؛ اجرا نمی‌شود"
