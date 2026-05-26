from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag_pipeline import get_answer
from src.blob_storage import list_blobs

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Banking Compliance Document Assistant",
    description="RAG-powered API for querying banking compliance and regulatory documents.",
    version="0.1.0",
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str


class DocumentListResponse(BaseModel):
    documents: list[str]


@app.get("/")
def root():
    """Root endpoint — redirects to docs."""
    return {"message": "Banking Compliance Document Assistant API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/documents", response_model=DocumentListResponse)
def get_documents():
    """List all documents stored in Azure Blob Storage."""
    try:
        blobs = list_blobs()
        return DocumentListResponse(documents=blobs)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """Ask a banking compliance question and receive a RAG-generated answer."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    try:
        answer = get_answer(request.question)
        return AnswerResponse(question=request.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))