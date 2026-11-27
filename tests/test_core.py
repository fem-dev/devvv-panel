from src.miner_catalog import get_miner, recommend_miners
from src.pool_config import PoolConfig, build_preview, validate_pool_config
from src.safe_runner import execution_status


def test_catalog_lookup_and_recommendations():
    assert get_miner("XMRig") is not None
    assert get_miner("not-a-miner") is None
    names = {item.name for item in recommend_miners(("NVIDIA",))}
    assert "XMRig" in names
    assert "BzMiner" in names


def test_pool_config_validation():
    good = PoolConfig("pool.example.org", 3333, "wallet12345678", "rig-01")
    assert validate_pool_config(good) == []
    bad = PoolConfig("https://bad host", 70000, "x", "bad worker!")
    assert len(validate_pool_config(bad)) >= 3


def test_preview_is_quoted_and_not_executed():
    config = PoolConfig("pool.example.org", 3333, "wallet12345678", "rig-01")
    preview = build_preview(config, "XMRig")
    assert "pool.example.org:3333" in preview
    assert "پیش‌نمایش" in preview
    assert execution_status()["running"] is False
