from ..register import register_provider_adapter
from .openai_source import ProviderOpenAIOfficial

ASTRAFLOW_DEFAULT_API_BASE = "https://api.umodelverse.com/v1"


@register_provider_adapter(
    "astraflow_chat_completion",
    "Astraflow (UModelverse) Chat Completion Provider Adapter",
    provider_display_name="Astraflow (UModelverse)",
    default_config_tmpl={
        "api_base": ASTRAFLOW_DEFAULT_API_BASE,
        "key": ["your-api-key-here"],
        "model": "gpt-4o-mini",
    },
)
class ProviderAstraflow(ProviderOpenAIOfficial):
    def __init__(
        self,
        provider_config: dict,
        provider_settings: dict,
    ) -> None:
        config = dict(provider_config)
        config.setdefault("api_base", ASTRAFLOW_DEFAULT_API_BASE)
        super().__init__(config, provider_settings)
