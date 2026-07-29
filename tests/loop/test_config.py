import importlib

import loop.config as config


def reload_config(monkeypatch, env):
    for key in ("LOOP_MODEL", "LOOP_TIER"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config)


def test_default_is_default_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {})
    assert cfg.resolve_model() == cfg.TIERS[cfg.DEFAULT_TIER]


def test_tier_env_selects_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "strong"})
    assert cfg.resolve_model() == cfg.TIERS["strong"]


def test_explicit_model_overrides_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "strong", "LOOP_MODEL": "custom-x"})
    assert cfg.resolve_model() == "custom-x"


def test_unknown_tier_falls_back_to_default(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "nonsense"})
    assert cfg.resolve_model() == cfg.TIERS[cfg.DEFAULT_TIER]
