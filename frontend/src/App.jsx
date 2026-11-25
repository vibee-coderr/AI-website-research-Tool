
import { useEffect, useState } from "react";
import {
  getStatus,
  processArticles,
  askQuestion
} from "./services/api";

import "./App.css";

function App() {
  const [urls, setUrls] = useState([""]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [status, setStatus] = useState("Checking...");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Check backend status
  const checkStatus = async () => {
    try {
      const res = await getStatus();
      setStatus(res.data.status);
    } catch {
      setStatus("Backend unavailable");
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  // Process article URLs
  const handleProcess = async () => {
    const validUrls = urls
      .map(url => url.trim())
      .filter(Boolean);

    if (!validUrls.length) {
      setMessage("Please enter at least one article URL.");
      return;
    }

    setLoading(true);
    setMessage("");
    setAnswer("");
    setSources([]);

    try {
      const res = await processArticles(validUrls);

      setMessage(
        `${res.data.message} ${res.data.chunks_created} chunks created.`
      );

      await checkStatus();

    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
        "Article processing failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  // Ask questions about processed articles
  const handleAsk = async () => {
    if (question.trim().length < 3) {
      setMessage("Please enter a question with at least 3 characters.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);
    setMessage("");

    try {
      const res = await askQuestion(question.trim());

      setAnswer(res.data.answer);
      setSources(res.data.sources || []);

    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
        "Unable to generate an answer. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">

      {/* Header */}
      <header>
        <p className="eyebrow">
          AI + RETRIEVAL AUGMENTED GENERATION
        </p>

        <h1>AI Article Research Assistant</h1>

        <p>
          Turn web articles into knowledge. Ask questions
          and get AI-powered answers with source references.
        </p>

        <span className="status">
          {status}
        </span>
      </header>

      {/* Article URL Section */}
      <section className="panel">
        <h2>1. Add Web Articles</h2>

        {urls.map((url, index) => (
          <input
            key={index}
            type="url"
            value={url}
            placeholder="https://example.com/article"
            onChange={e =>
              setUrls(old =>
                old.map((item, i) =>
                  i === index ? e.target.value : item
                )
              )
            }
          />
        ))}

        <button
          className="secondary"
          disabled={urls.length >= 5 || loading}
          onClick={() =>
            setUrls(old => [...old, ""])
          }
        >
          + Add URL
        </button>

        <button
          onClick={handleProcess}
          disabled={loading}
        >
          {loading ? "Processing..." : "Process Articles"}
        </button>
      </section>

      {/* Question Section */}
      <section className="panel">
        <h2>2. Ask Questions About Your Articles</h2>

        <textarea
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="What are the important points mentioned in these articles?"
        />

        <button
          onClick={handleAsk}
          disabled={loading}
        >
          {loading ? "Please wait..." : "Ask AI"}
        </button>
      </section>

      {/* Status Messages */}
      {message && (
        <p className="message">
          {message}
        </p>
      )}

      {/* Generated Answer */}
      {answer && (
        <section className="panel">
          <h2>AI Generated Answer</h2>

          <p className="answer">
            {answer}
          </p>

          <h3>Retrieved Sources</h3>

          {sources.map((source, index) => (
            <article
              className="source"
              key={index}
            >
              <strong>
                {source.source_id}
              </strong>

              <p>
                {source.content.slice(0, 350)}
                {source.content.length > 350 ? "..." : ""}
              </p>

              {source.url !== "Unknown" && (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Read Article
                </a>
              )}
            </article>
          ))}
        </section>
      )}

      {/* Footer */}
      <footer>
        <p>
          Powered by FastAPI, LangChain, FAISS and Ollama
        </p>
      </footer>

    </main>
  );
}

export default App;
