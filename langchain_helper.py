from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

def load_data(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    return data


def split_data(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(data)
    return docs


def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings


def create_vectorstore(docs, embeddings):
    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )
    return vectorstore



def answer_question(vectorstore, question):
    docs = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    prompt = f"""
    Answer the question using only the given news content.

    Use simple and clear language.
    Do not add information from outside the articles.
    If the answer is not available, say so clearly.

    News content:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content, docs
