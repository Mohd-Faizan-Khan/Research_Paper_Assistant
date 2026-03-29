from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your modules
from retrieval.semantic_search import search
from rag.rag_pipeline import ask_question
from rag.paper_explainer import explain_paper


app = FastAPI(title="Research Paper AI")


# -----------------------------
# Request Models
# -----------------------------

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class AskRequest(BaseModel):
    question: str


class ExplainRequest(BaseModel):
    text: str


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Semantic Search
# -----------------------------

@app.post("/search")
def semantic_search(request: SearchRequest):
    results = search(request.query, request.top_k)

    return {
        "query": request.query,
        "results": results
    }


# -----------------------------
# RAG Question Answering
# -----------------------------

@app.post("/ask")
def ask_ai(request: AskRequest):
    result = ask_question(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }


# -----------------------------
# Paper Explainer
# -----------------------------

@app.post("/explain")
def explain(request: ExplainRequest):

    results = search(request.text)

    if not results:
        return {"error": "No papers found"}

    paper = results[0]

    explanation = explain_paper(
        paper["title"],
        paper["abstract"]
    )

    return {
        "title": paper["title"],
        "explanation": explanation,
        "pdf_url": paper["pdf_url"]
    }