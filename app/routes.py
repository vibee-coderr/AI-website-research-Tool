
import logging
import requests

from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, Field

from app import rag_pipeline as p
from app.config import FAISS_INDEX_PATH


logger = logging.getLogger(__name__)

router = APIRouter()

# Store FAISS vector database in memory
vectorstore = None


# Load previously saved vector database
def load_existing_vectorstore():
    global vectorstore

    try:
        vectorstore = p.load_saved_vectorstore()
        logger.info("Existing FAISS vectorstore loaded successfully.")

    except Exception as e:
        vectorstore = None
        logger.warning("No existing FAISS vectorstore found: %s", e)


# Request model for article URLs
class URLRequest(BaseModel):
    urls: List[HttpUrl] = Field(
        min_length=1,
        max_length=5,
        description="Provide between 1 and 5 article URLs"
    )


# Request model for questions
class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500,
        description="Enter a question about the processed articles"
    )


# Process article URLs
@router.post("/process-urls")
def process_urls(request: URLRequest):
    global vectorstore

    try:
        urls = [str(url) for url in request.urls]

        data = p.load_data(urls)

        if not data:
            raise HTTPException(
                status_code=422,
                detail="Unable to extract content from the URLs."
            )

        docs = p.split_data(data)

        if not docs:
            raise HTTPException(
                status_code=422,
                detail="No usable text chunks were created."
            )

        embeddings = p.create_embeddings()

        new_vectorstore = p.create_vectorstore(
            docs, embeddings
        )

        new_vectorstore.save_local(FAISS_INDEX_PATH)

        vectorstore = new_vectorstore

        return {
            "message": "Articles processed successfully!",
            "articles_loaded": len(data),
            "chunks_created": len(docs),
            "vectors_stored": vectorstore.index.ntotal
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Article processing failed")

        raise HTTPException(
            status_code=500,
            detail="Article processing failed. Check the server logs."
        )


# Ask questions about processed articles
@router.post("/ask")
def ask_question(request: QuestionRequest):

    if vectorstore is None:
        raise HTTPException(
            status_code=400,
            detail="Please process articles before asking questions."
        )

    try:
        answer, source_docs = p.answer_question(
            vectorstore,
            request.question
        )

        sources = [
            {
                "source_id": f"Source {i}",
                "url": doc.metadata.get("source", "Unknown"),
                "content": doc.page_content
            }
            for i, doc in enumerate(source_docs, start=1)
        ]

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception:
        logger.exception("Question answering failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate an answer. Check Ollama and server logs."
        )


# Check vector database status
@router.get("/status")
def get_status():

    if vectorstore is None:
        return {
            "status": "Not Ready",
            "message": "Please process articles first.",
            "vectors_stored": 0
        }

    return {
        "status": "Ready",
        "message": "AI Article Research Assistant is ready!",
        "vectors_stored": vectorstore.index.ntotal
    }


# Check API and Ollama health
@router.get("/health")
def health_check():

    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3
        )

        response.raise_for_status()

        return {
            "api": "Running",
            "ollama": "Running",
            "status": "Healthy"
        }

    except requests.RequestException:

        return {
            "api": "Running",
            "ollama": "Not Available",
            "status": "Unhealthy"
        }
