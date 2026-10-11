# Simple PDF RAG Lab (Free Models)

A beginner-friendly Retrieval-Augmented Generation (RAG) lab for AI students.
Upload a PDF, index its text, and ask questions based on retrieved passages.

## Files
- `app.py` — Streamlit front end
- `rag_core.py` — PDF extraction, chunking, embeddings, retrieval, and generation
- `requirements.txt` — Python dependencies

## Free models used
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Text generation: `google/flan-t5-small` (Apache-2.0 license)

No paid API key is required. Models are downloaded from Hugging Face on first run.
This is not unlimited hosted GPT access: free cloud services have resource limits, and
this app runs models within the CPU/RAM available to the deployment. Answers may be
basic because FLAN-T5-small is a small teaching model.

## Run locally
Python 3.10 or 3.11 is recommended.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## Upload to GitHub
1. Sign in at https://github.com and click **New repository**.
2. Name it `simple-pdf-rag-lab`.
3. Choose **Public** if you want free public Streamlit Community Cloud deployment.
4. Create the repository.
5. Click **Add file → Upload files**.
6. Upload `app.py`, `rag_core.py`, `requirements.txt`, and `README.md`.
7. Click **Commit changes**.

Do not upload private PDFs, passwords, API keys, or confidential documents.

## Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io and sign in with GitHub.
2. Click **Create app**.
3. Select your repository (`simple-pdf-rag-lab`), branch (`main`), and main file path `app.py`.
4. Click **Deploy**.
5. The first startup downloads the models and may take several minutes.

If deployment fails due to memory or build limits, try running locally or in Google Colab.
Free hosted resources can change and are not guaranteed to be unlimited.

## How to teach the RAG pipeline
1. **Load:** `extract_pdf_text()` reads selectable text from the PDF.
2. **Chunk:** `split_text()` breaks the text into overlapping sections.
3. **Embed:** SentenceTransformer turns each chunk into a vector.
4. **Retrieve:** cosine similarity (dot product of normalized vectors) selects the most relevant chunks.
5. **Generate:** FLAN-T5 receives the question plus retrieved context and writes an answer.

The model is not trained on the PDF. The PDF is indexed so relevant passages can be retrieved at question time.

## Limitations
- Scanned/image-only PDFs need OCR first.
- This is a minimal educational example, not a production-secure service.
- Streamlit Community Cloud has CPU/RAM limits; model loading and answers may be slow.
- Do not treat answers as guaranteed factual; inspect the retrieved chunks.
