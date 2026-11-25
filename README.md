# AI Equity Research Tool

An AI-powered news research application that helps users understand financial and business news by asking questions about articles.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from news articles and generate answers using a locally running language model.

## Features

- Load news articles using URLs.
- Extract and split article content into smaller text chunks.
- Generate text embeddings using HuggingFace.
- Store and retrieve relevant information using FAISS.
- Ask questions about the processed news articles.
- Generate answers using Ollama (Llama 3.2).
- View the retrieved source content and original article links.
- Simple dark-themed interface built with Streamlit.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | User interface |
| LangChain | RAG pipeline |
| HuggingFace | Text embeddings |
| FAISS | Vector storage and similarity search |
| Ollama | Local language model |
| Llama 3.2 (3B) | Answer generation |

## How It Works

1. The user enters news article URLs.
2. The application extracts the article content.
3. The extracted text is divided into smaller chunks.
4. HuggingFace generates embeddings for the text chunks.
5. FAISS stores the embeddings for similarity search.
6. When a question is entered, relevant chunks are retrieved.
7. The retrieved content is passed to the Llama 3.2 model through Ollama.
8. The model generates an answer based on the retrieved news content.

### OUTPUTS 

<br>
<img width="1277" height="599" alt="image" src="https://github.com/user-attachments/assets/5c833118-68c2-47dd-bdc9-11e86db0e86d" />
<br>
<img width="1279" height="598" alt="image" src="https://github.com/user-attachments/assets/c662d58b-5ff4-4573-b466-c2232ef217c3" />
<br>
<img width="1277" height="599" alt="image" src="https://github.com/user-attachments/assets/b9ac0fd9-0a1a-48f8-b1ae-21db0cdcab5f" />


## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/vibee-coderr/AI-Equity-Research-Tool-.git
```

### 2. Navigate to the project folder

```bash
cd AI-Equity-Research-Tool-
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Ollama

Download Ollama from:

https://ollama.com/download/windows

Pull the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting the application.

### 6. Run the application

```bash
streamlit run main.py
```

The application will open in your browser.

## Usage

1. Open the application.
2. Enter one or more news article URLs in the sidebar.
3. Click **Process Articles**.
4. Wait for the articles to be processed and stored in FAISS.
5. Enter a question related to the processed articles.
6. Click **Generate Answer**.
7. View the generated answer and retrieved source content.

## Note

- An internet connection is required to load news articles and download the embedding model when needed.
- Ollama runs the language model locally.
- Answer quality depends on the content extracted from the provided articles.
- This project focuses on news-based research and does not provide financial advice or stock price predictions.

## Future Improvements

- Improve news article extraction.
- Support more financial news sources.
- Improve source referencing and retrieval accuracy.

---

**Developed as a learning project to explore Retrieval-Augmented Generation, vector databases, and local language models.**
