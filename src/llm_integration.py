from langchain_openai import AzureChatOpenAI

from src.config_loader import get_azure_openai_config


def get_llm_model() -> AzureChatOpenAI:
    """Return an Azure OpenAI chat model instance."""
    cfg = get_azure_openai_config()
    return AzureChatOpenAI(
        azure_deployment=cfg["chat_deployment"],
        azure_endpoint=cfg["azure_endpoint"],
        api_key=cfg["api_key"],
        api_version=cfg["api_version"],
        temperature=cfg["temperature"],
    )

