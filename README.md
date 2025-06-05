# Local RAG with Ollama

![Ollama title slide](GettingStarted/a.png)


This is a fully local Retrieval-Augmented Generation (RAG) system using:

- Ollama (`llama3.1:latest` and `nomic-embed-text`)
- ChromaDB for vector storage
- PyMuPDF (`fitz`) for PDF parsing
- A terminal-based chat interface

## 🔧 Setup

> --- NOTE: While working in our lab - both steps 1 and 2 below have alredy been done for you. ---
> --- You should start with setup step #3 while running this in the UTCS Lab.

### 1. Install Dependencies

Use the following in your Conda environment:

```bash
pip install pymupdf chromadb tqdm termcolor langchain scikit-learn
```

### 2. Install Ollama

- **Ubuntu**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
- **macOS**:
```bash
brew install ollama
```
- **Windows**:
Download from https://ollama.com/download and install.

### 3. Then pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:latest
```

## 📂 Project Structure

```
rag_local_ollama/
├── GettingStarted/         # Lab guide we'll walk through in class
├── docs/                   # Place your PDFs here
├── test_and_qa-Scripts/    # Extra testing scripts used for build - you won't need these
├── ingested.json           # Tracks processed PDFs
├── pdf_loader.py           # PDF chunking logic
├── embedder.py             # Embedding via Ollama
├── retriever.py            # ChromaDB vector store + reranking
├── ollama_runner.py        # LLM prompt handling via Ollama
├── chat_loop.py            # Terminal input/output
├── pdf_manager.py          # Handles new PDF detection
├── rag_pipeline.py         # Main entrypoint
```

## 🚀 Run It

```bash
python rag_pipeline.py
```

Place any PDFs in the `docs/` directory. They’ll be automatically processed and embedded.
This RAG is updatable and supports multiple PDF's. 
- You can drop as many PDFs as you want into the docs/ folder.
- The `pdf_manager.py` script will only process the new ones by using `ingested.json` to remember what’s been done already.
- This ensure efficient use of embedding resources on your machine and only embedding new PDF's.

## ❓ Ask Questions

Ask a question in the terminal. Type `exit` to quit.

---

This project is designed for use in Ubuntu, but works equally on macOS and Windows.
