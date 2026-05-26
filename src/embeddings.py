from langchain_openai import AzureOpenAIEmbeddings

from src.config_loader import get_azure_openai_config


def get_embedding_model() -> AzureOpenAIEmbeddings:
    """Return an Azure OpenAI embedding model instance."""
    cfg = get_azure_openai_config()
    return AzureOpenAIEmbeddings(
        azure_deployment=cfg["embedding_deployment"],
        azure_endpoint=cfg["azure_endpoint"],
        api_key=cfg["api_key"],
        api_version=cfg["api_version"],
    )
