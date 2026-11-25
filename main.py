
import streamlit as st
import langchain_helper as p

# Page configuration
st.set_page_config(
    page_title="Equity Research AI",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #A78BFA;
}
.subtitle {
    color: #94A3B8;
    font-size: 16px;
}
.stButton button {
    background-color: #7C3AED;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}
.stButton button:hover {
    background-color: #6D28D9;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">Equity Research AI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">AI-powered financial news research assistant</div>',
    unsafe_allow_html=True
)

st.divider()

# Sidebar
st.sidebar.title("📄 News Sources")
st.sidebar.write("Add news article URLs below.")

url1 = st.sidebar.text_input("Article URL 1")
url2 = st.sidebar.text_input("Article URL 2")
url3 = st.sidebar.text_input("Article URL 3")

process = st.sidebar.button(
    "Process Articles",
    use_container_width=True
)

# Process articles
if process:
    urls = [url1, url2, url3]
    urls = [url for url in urls if url.strip()]

    if not urls:
        st.warning("Please enter at least one article URL.")

    else:
        try:
            with st.spinner("Processing articles..."):

                data = p.load_data(urls)
                docs = p.split_data(data)

                if not docs:
                    st.warning("No article content was extracted.")

                else:
                    embeddings = p.create_embeddings()
                    vectorstore = p.create_vectorstore(
                        docs, embeddings
                    )

                    st.session_state.vectorstore = vectorstore
                    st.session_state.article_count = len(data)
                    st.session_state.chunk_count = len(docs)

                    vectorstore.save_local("faiss_index")

                    st.success("Articles processed successfully!")

        except Exception as e:
            st.error(f"Error processing articles: {e}")

# Dashboard metrics
st.subheader("Research Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Articles Loaded",
        st.session_state.get("article_count", 0)
    )

with col2:
    st.metric(
        "Text Chunks",
        st.session_state.get("chunk_count", 0)
    )

with col3:
    status = "Ready" if "vectorstore" in st.session_state else "Waiting"
    st.metric("AI Status", status)

st.divider()

# Question answering
st.subheader("Ask Your Research Question")

question = st.text_input(
    "Enter your question",
    placeholder="What is the latest news about NVIDIA?"
)

if st.button("Generate Answer", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question.")

    elif "vectorstore" not in st.session_state:
        st.warning("Please process articles first.")

    else:
        try:
            with st.spinner("AI is analyzing the news..."):

                answer, source_docs = p.answer_question(
                    st.session_state.vectorstore,
                    question
                )

            st.markdown("### AI Research Answer")
            st.write(answer)

            
            with st.expander("View Sources"):
                for i, doc in enumerate(source_docs):
                    st.markdown(f"**Source {i + 1}**")

                    source_url = doc.metadata.get("source")

                    if source_url:
                        st.write("Article:", source_url)

                        st.write(doc.page_content)
                        st.divider()


        except Exception as e:
            st.error(f"Error generating answer: {e}")

st.divider()

st.caption("Powered by LangChain • FAISS • HuggingFace • Ollama")
