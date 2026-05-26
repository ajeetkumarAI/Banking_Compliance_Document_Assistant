# Banking Compliance Document Assistant

A FastAPI-based Banking Compliance assistant that uses a RAG (Retrieval-Augmented Generation) pipeline powered by **Azure OpenAI**, **Azure Blob Storage**, and **Azure AI Search** to answer questions about uploaded banking compliance and regulatory documents.

## Features

- Upload banking compliance and regulatory PDFs to **Azure Blob Storage**
- Automatic document chunking and embedding via **Azure OpenAI**
- Vector storage and retrieval with **Azure AI Search**
- Context-aware answers grounded in the uploaded documents
- REST API with interactive Swagger docs at `/docs`

## Prerequisites

- Python 3.11+
- Docker (optional, for containerised deployment)
- An **Azure** subscription with the following resources provisioned:
  - [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/) — with a **chat deployment** (e.g. `gpt-4o-mini`) and an **embedding deployment** (e.g. `text-embedding-3-small`)
  - [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/) — a storage account with a container for compliance documents
  - [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/) — a search service for vector indexing

## Setup

### Local

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Windows (Command Prompt)
   venv\Scripts\activate.bat
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Azure credentials:**

   Copy the example file and fill in your values:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your Azure keys:

   ```env
   # Azure OpenAI
   AZURE_OPENAI_API_KEY=your-azure-openai-api-key
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/

   # Azure Blob Storage
   AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net

   # Azure AI Search
   AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
   AZURE_SEARCH_API_KEY=your-azure-search-api-key
   ```

4. **Update deployment names (if different):**

   Edit `config/config.yaml` and set the `chat_deployment`, `embedding_deployment`, `container_name`, and `index_name` to match the names you created in the Azure portal.

5. **Run the server:**

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

   Open http://localhost:8000/docs for the interactive Swagger UI.

### Docker

```bash
docker build -t banking-compliance-assistant .
az acr login --name mcr121 -g myrg1 
docker tag banking-compliance-assistant mcr121.azurecr.io/banking-compliance-assistant:latest
docker push mcr121.azurecr.io/banking-compliance-assistant:latest


docker run --env-file .env -p 8000:8000 banking-compliance-assistant
```

Open http://localhost:8000/docs for the interactive Swagger UI.

## API Endpoints

| Method | Path         | Description                                      |
|--------|--------------|--------------------------------------------------|
| GET    | `/health`    | Health check                                     |
| GET    | `/documents` | List all documents in Azure Blob Storage         |
| POST   | `/ask`       | Ask a banking compliance question (JSON body)    |

### Example — Ask a question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the KYC requirements for new account opening?"}'
```

## Architecture

```
User uploads PDF
      │
      ▼
Azure Blob Storage  ←  PDF stored for durable backup
      │
      ▼
PyMuPDF  →  Chunking  →  Azure OpenAI Embeddings
                                │
                                ▼
                        Azure AI Search  ←  vectors indexed
                                │
                    user asks a question
                                │
                                ▼
                        Azure AI Search  →  top-k relevant chunks
                                │
                                ▼
                        Azure OpenAI Chat  →  answer
```

## Project Structure

```
app.py                  # FastAPI entry point
Dockerfile              # Container image definition
src/
  config_loader.py      # Centralised config + env-var loader
  document_loaders.py   # PDF loading via PyMuPDF
  chunking.py           # Recursive text splitting
  embeddings.py         # Azure OpenAI embedding model
  vectorstore.py        # Azure AI Search vector store
  llm_integration.py    # Azure OpenAI chat model wrapper
  blob_storage.py       # Azure Blob Storage upload / download / list
  rag_pipeline.py       # Indexing and QA orchestration
prompts/
  prompt_template.py    # System/user prompt builder
config/
  config.yaml           # Centralised configuration values
data/sample_pdfs/       # Local staging area for uploaded PDFs
.env.example            # Template for required environment variables
```
