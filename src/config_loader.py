import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()


def load_config() -> dict:
    """Load configuration from config/config.yaml."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_azure_openai_config() -> dict:
    """Return Azure OpenAI connection details from env vars + config."""
    cfg = load_config()["azure_openai"]
    return {
        "api_key": os.environ["AZURE_OPENAI_API_KEY"],
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": cfg["api_version"],
        "chat_deployment": cfg["chat_deployment"],
        "embedding_deployment": cfg["embedding_deployment"],
        "temperature": cfg["temperature"],
    }


def get_azure_blob_config() -> dict:
    """Return Azure Blob Storage connection details."""
    cfg = load_config()["azure_blob_storage"]
    return {
        "connection_string": os.environ["AZURE_STORAGE_CONNECTION_STRING"],
        "container_name": cfg["container_name"],
    }


def get_azure_search_config() -> dict:
    """Return Azure AI Search connection details."""
    cfg = load_config()["azure_search"]
    return {
        "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
        "api_key": os.environ["AZURE_SEARCH_API_KEY"],
        "index_name": cfg["index_name"],
        "fields": cfg.get("fields", {}),
    }


def get_chunking_config() -> dict:
    """Return chunking configuration."""
    return load_config()["chunking"]


def get_retriever_config() -> dict:
    """Return retriever configuration."""
    return load_config()["retriever"]
