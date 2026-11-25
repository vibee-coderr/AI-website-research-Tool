
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

from app.config import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    RETRIEVAL_K
)


# Load article content from URLs
def load_data(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    return data


# Split articles into smaller chunks
def split_data(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(data)
    return docs


# Create embeddings
def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )
    return embeddings


# Create FAISS vector database
def create_vectorstore(docs, embeddings):
    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )
    return vectorstore


# Generate answers using RAG
def answer_question(vectorstore, question):

    docs = vectorstore.similarity_search(
        question,
        k=RETRIEVAL_K
    )

    if not docs:
        return "No relevant information found.", []

    context_parts = []

    for i, doc in enumerate(docs, start=1):
        source_url = doc.metadata.get("source", "Unknown source")

        context_parts.append(
            f"""
            [Source {i}]
            Article URL: {source_url}
            Content: {doc.page_content}
            """
        )

    context = "\n\n".join(context_parts)

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0
    )

    prompt = f"""
    You are an AI Article Research Assistant.

    Answer the question using only the provided article content.

    Instructions:
    1. Use simple and clear language.
    2. Do not add information from outside the articles.
    3. Cite your answer using [Source 1], [Source 2], etc.
    4. Only cite sources that support your statements.
    5. If the answer is unavailable, clearly say so.
    6. Do not invent facts or source references.

    Article Content:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content, docs


# Load previously saved FAISS vector database
def load_saved_vectorstore():
    embeddings = create_embeddings()

    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore
