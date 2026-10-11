import streamlit as st
from rag_core import read_pdf, split_into_chunks, build_index, retrieve, generate_answer

st.set_page_config(page_title="Free PDF RAG Lab", page_icon="📚", layout="wide")
st.title("📚 Free PDF RAG Lab")
st.write("Upload a PDF, build a searchable knowledge base, and ask questions grounded in the document.")
st.info("No paid API or API key is used. Answer generation uses the open-weight FLAN-T5-small model. The first answer may take longer while model weights download. Free hosting has compute/memory limits, so unlimited usage cannot be guaranteed.")
with st.sidebar:
    st.header("RAG settings")
    chunk_words = st.slider("Words per chunk", 80, 280, 160, 10)
    overlap_words = st.slider("Chunk overlap", 0, 60, 30, 5)
    top_k = st.slider("Relevant chunks", 1, 5, 3)

pdf = st.file_uploader("Upload a text-based PDF", type=["pdf"])
if pdf and st.button("Read PDF and build knowledge base", type="primary"):
    try:
        with st.spinner("Extracting text and building index..."):
            pages = read_pdf(pdf)
            chunks = split_into_chunks(pages, chunk_words, overlap_words)
            vectorizer, matrix = build_index(chunks)
        st.session_state["rag"] = {"filename": pdf.name, "pages": pages, "chunks": chunks, "vectorizer": vectorizer, "matrix": matrix}
        st.success("Knowledge base is ready.")
    except Exception as e:
        st.error(f"PDF processing failed: {e}")

rag = st.session_state.get("rag")
if rag:
    a, b, c = st.columns(3)
    a.metric("Document", rag["filename"]); b.metric("Pages with text", len(rag["pages"])); c.metric("Chunks", len(rag["chunks"]))
    question = st.text_input("Ask a question about your PDF")
    if st.button("Generate answer"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            try:
                with st.spinner("Retrieving passages and generating answer..."):
                    results = retrieve(question, rag["chunks"], rag["vectorizer"], rag["matrix"], top_k)
                    answer = generate_answer(question, results)
                st.subheader("Answer"); st.write(answer)
                st.subheader("Retrieved source passages")
                if not results: st.write("No relevant passages found.")
                for i, r in enumerate(results, 1):
                    st.markdown(f"**Source {i} — PDF page {r['page']} — similarity {r['score']:.3f}**")
                    st.write(r["text"]); st.divider()
            except Exception as e:
                st.error(f"Generation failed: {e}. Try a smaller PDF or run locally with more memory.")
else:
    st.markdown("**Workflow:** upload PDF → build index → ask question → verify the answer against the source passages.")
