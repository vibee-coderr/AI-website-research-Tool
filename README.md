# AI Article Research Assistant

An AI-powered research assistant that extracts content from web articles and answers user questions using **Retrieval-Augmented Generation (RAG)**.

The application uses LangChain, HuggingFace embeddings, FAISS vector search and a locally running LLM through Ollama. It provides a React frontend and FastAPI backend for an interactive article research experience.

## Features

- **Article Processing:** Extract text from web articles using their URLs.
- **Text Chunking:** Split extracted content into smaller chunks for efficient retrieval.
- **Semantic Search:** Generate embeddings using HuggingFace sentence-transformer models.
- **Vector Database:** Store and retrieve article embeddings using FAISS.
- **AI-Powered Answers:** Generate context-aware answers using Ollama and Llama 3.2.
- **Source References:** Display retrieved article sources alongside generated answers.
- **Persistent Storage:** Save and reload the FAISS vector database.
- **REST API:** Manage article processing and question answering through FastAPI.
- **Interactive Frontend:** Use a React interface to process articles and ask questions.

## Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| API Communication | Axios |
| LLM Framework | LangChain |
| Language Model | Ollama, Llama 3.2 (3B) |
| Embeddings | HuggingFace, all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Article Extraction | UnstructuredURLLoader |
| Validation | Pydantic |

## System Architecture

```text
             User
              |
              v
       React Frontend
              |
           Axios
              |
              v
       FastAPI Backend
              |
       Article Processing
              |
              v
       UnstructuredURLLoader
              |
              v
        Text Chunking
              |
              v
     HuggingFace Embeddings
              |
              v
        FAISS Vector DB
              |
        User Question
              |
              v
       Semantic Search
              |
              v
       Relevant Chunks
              |
              v
        Ollama LLM
         Llama 3.2
              |
              v
      Generated Answer
              |
              v
      Sources + Answer
         React UI
```

## Project Structure

```text
AI-Article-Research-Assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── rag_pipeline.py
│   └── config.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── faiss_index/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vibee-coderr/AI-Equity-Research-Tool-.git
cd AI-Equity-Research-Tool-
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Download Ollama from:

https://ollama.com/

Download the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before asking questions.

### 5. Start the FastAPI Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 6. Set Up the React Frontend

Open another terminal:

```bash
cd frontend
npm install
```

Start the frontend:

```bash
npm run dev
```

Open the local URL displayed in your terminal, usually:

`http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/health` | Check API and Ollama availability |
| GET | `/status` | Check vector database status |
| POST | `/process-urls` | Extract and process article URLs |
| POST | `/ask` | Ask questions about processed articles |

### Example: Process Articles

**POST** `/process-urls`

Request:

```json
{
  "urls": [
    "https://example.com/article"
  ]
}
```

### Example: Ask a Question

**POST** `/ask`

Request:

```json
{
  "question": "What are the main points discussed in the article?"
}
```

The response includes the generated answer and retrieved source references.


## Working Outputs

<img width="1279" height="602" alt="image" src="https://github.com/user-attachments/assets/01bb1f53-293e-4a6f-87be-1fc10c30b684" />
<br>
<br>
<img width="1279" height="603" alt="image" src="https://github.com/user-attachments/assets/fff4f45e-84c3-4912-b3ce-04b92110f322" />
<br>
<br>
<img width="1279" height="605" alt="image" src="https://github.com/user-attachments/assets/8a581fa5-8b78-44f9-80d1-34a91f874c8a" />
<br>
<br>

## How It Works

1. The user provides article URLs through the React interface.
2. FastAPI receives the URLs and extracts article content.
3. The extracted content is divided into smaller text chunks.
4. HuggingFace generates vector embeddings for the chunks.
5. FAISS stores the embeddings for semantic retrieval.
6. When a user asks a question, FAISS retrieves relevant chunks.
7. The retrieved context is passed to the Llama 3.2 model through Ollama.
8. The model generates an answer using the provided article content.
9. The answer and source references are displayed in React.

## Important Notes

- The application is designed to run locally.
- Ollama and the required language model must be installed separately.
- The FAISS index is generated locally and is not included in the GitHub repository.
- Process article URLs again to generate a new index if one is not available.
- Article extraction depends on website accessibility and page structure. Some websites may restrict automated extraction.
- The project uses local embeddings and a local LLM, avoiding paid API requirements.

## Future Improvements

- Conversation history for follow-up questions.
- Improved retrieval using hybrid search.
- Support for PDF document uploads.
- Streaming AI responses.
- Better article metadata and source management.

## Author

**Kamalesh R**

B.Tech – Artificial Intelligence and Data Science

GitHub: https://github.com/vibee-coderr

---

*Built to explore Retrieval-Augmented Generation, semantic search, local LLMs and full-stack AI application development.*
