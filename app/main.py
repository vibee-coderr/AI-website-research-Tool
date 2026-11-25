
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router, load_existing_vectorstore


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_existing_vectorstore()
    yield


app = FastAPI(
    title="AI Article Research Assistant",
    description="An AI-powered research assistant that extracts information from web articles and answers user questions using Retrieval-Augmented Generation (RAG), semantic search, and locally running Large Language Models.",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Equity Research API is running!"
    }
