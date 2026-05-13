import pytest

from astrbot.core.provider.sources.astraflow_source import (
    ASTRAFLOW_DEFAULT_API_BASE,
    ProviderAstraflow,
)
from astrbot.core.provider.register import provider_cls_map


def _make_provider(overrides: dict | None = None) -> ProviderAstraflow:
    provider_config = {
        "id": "test-astraflow",
        "type": "astraflow_chat_completion",
        "model": "gpt-4o-mini",
        "key": ["test-key"],
    }
    if overrides:
        provider_config.update(overrides)
    return ProviderAstraflow(
        provider_config=provider_config,
        provider_settings={},
    )


def test_astraflow_registered_in_provider_registry():
    assert "astraflow_chat_completion" in provider_cls_map


def test_astraflow_display_name():
    meta = provider_cls_map["astraflow_chat_completion"]
    assert meta.provider_display_name == "Astraflow (UModelverse)"


def test_astraflow_default_config_tmpl_has_api_base():
    meta = provider_cls_map["astraflow_chat_completion"]
    assert meta.default_config_tmpl is not None
    assert meta.default_config_tmpl["api_base"] == ASTRAFLOW_DEFAULT_API_BASE


@pytest.mark.asyncio
async def test_astraflow_uses_default_api_base_when_not_provided():
    provider = _make_provider()
    try:
        assert provider.base_url == ASTRAFLOW_DEFAULT_API_BASE or (
            hasattr(provider, "provider_config")
            and provider.provider_config.get("api_base") == ASTRAFLOW_DEFAULT_API_BASE
        )
    finally:
        await provider.terminate()


@pytest.mark.asyncio
async def test_astraflow_respects_custom_api_base():
    custom_base = "https://custom.example.com/v1"
    provider = _make_provider({"api_base": custom_base})
    try:
        assert provider.provider_config.get("api_base") == custom_base
    finally:
        await provider.terminate()


@pytest.mark.asyncio
async def test_astraflow_does_not_mutate_original_config():
    original_config = {
        "id": "test-astraflow",
        "type": "astraflow_chat_completion",
        "model": "gpt-4o-mini",
        "key": ["test-key"],
    }
    provider = ProviderAstraflow(
        provider_config=original_config,
        provider_settings={},
    )
    try:
        assert "api_base" not in original_config
    finally:
        await provider.terminate()
