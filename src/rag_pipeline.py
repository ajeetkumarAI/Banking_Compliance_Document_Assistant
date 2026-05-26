from src.embeddings import get_embedding_model
from src.vectorstore import load_vector_store, get_retriever
from src.llm_integration import get_llm_model
from prompts.prompt_template import build_prompt


def get_answer(question: str) -> str:
    """Retrieve relevant context from Azure AI Search and return an LLM-generated answer."""
    embedding_model = get_embedding_model()
    vector_store = load_vector_store(embedding_model)
    retriever = get_retriever(vector_store)

    relevant_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    prompt = build_prompt(context, question)
    llm = get_llm_model()
    response = llm.invoke(prompt)
    return response.content