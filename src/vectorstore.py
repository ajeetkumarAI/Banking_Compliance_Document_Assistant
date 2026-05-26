import langchain_community.vectorstores.azuresearch as _az_module
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

from src.config_loader import get_azure_search_config

# Override LangChain's default field names with the ones from config.yaml
# so they match the existing Azure AI Search index schema.


# FIELDS_ID → "chunk_id" (your key field)
# FIELDS_CONTENT → "chunk" (your text content field)
# FIELDS_CONTENT_VECTOR → "text_vector" (your embedding vector field)


_fields = get_azure_search_config().get("fields", {})
if _fields.get("id"):
    _az_module.FIELDS_ID = _fields["id"]
if _fields.get("content"):
    _az_module.FIELDS_CONTENT = _fields["content"]
if _fields.get("content_vector"):
    _az_module.FIELDS_CONTENT_VECTOR = _fields["content_vector"]


def _get_azure_search_store(embeddings: Embeddings) -> AzureSearch:
    """Return an AzureSearch vector store instance."""
    cfg = get_azure_search_config()
    return AzureSearch(
        azure_search_endpoint=cfg["endpoint"],
        azure_search_key=cfg["api_key"],
        index_name=cfg["index_name"],
        embedding_function=embeddings,
    )


def load_vector_store(embeddings: Embeddings) -> AzureSearch:
    """Return a handle to the existing Azure AI Search index."""
    return _get_azure_search_store(embeddings)


def get_retriever(vector_store: AzureSearch) -> VectorStoreRetriever:
    """Return a retriever from the Azure AI Search vector store."""
    return vector_store.as_retriever(
        search_type="similarity",
    )