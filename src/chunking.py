from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config_loader import get_chunking_config


def chunk_documents(docs: list[Document]) -> list[Document]:
    """Split documents into smaller chunks for embedding."""
    cfg = get_chunking_config()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["chunk_size"],
        chunk_overlap=cfg["chunk_overlap"],
        separators=["\n\n", "\n", "(?<=. )", " ", ""],
    )
    return text_splitter.split_documents(docs)
