import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient

from src.config_loader import get_azure_blob_config

def list_blobs() -> list[str]:
    """List all blob names in the configured container."""
    cfg = get_azure_blob_config()
    blob_service = BlobServiceClient.from_connection_string(cfg["connection_string"])
    container_client = blob_service.get_container_client(cfg["container_name"])
    return [blob.name for blob in container_client.list_blobs()]


# def upload_to_blob(local_path: str) -> str:
#     """Upload a local file to Azure Blob Storage and return the blob name."""
#     cfg = get_azure_blob_config()
#     blob_service = BlobServiceClient.from_connection_string(cfg["connection_string"])
#     container_client = blob_service.get_container_client(cfg["container_name"])

#     blob_name = Path(local_path).name
#     with open(local_path, "rb") as data:
#         container_client.upload_blob(name=blob_name, data=data, overwrite=True)

#     return blob_name


# def download_from_blob(blob_name: str, download_dir: str = "data/sample_pdfs") -> str:
#     """Download a blob to a local directory and return the local file path."""
#     cfg = get_azure_blob_config()
#     blob_service = BlobServiceClient.from_connection_string(cfg["connection_string"])
#     container_client = blob_service.get_container_client(cfg["container_name"])

#     os.makedirs(download_dir, exist_ok=True)
#     local_path = os.path.join(download_dir, blob_name)

#     blob_client = container_client.get_blob_client(blob_name)
#     with open(local_path, "wb") as f:
#         stream = blob_client.download_blob()
#         f.write(stream.readall())

#     return local_path