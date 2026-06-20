import os
import re
import fitz  # pymupdf
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

_collection = None


# ── Document loading ──────────────────────────────────────────────────────────

def _load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _load_pdf(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def _load_all_docs(docs_dir: str) -> list[dict]:
    """Return list of {source, text} dicts for every .txt and .pdf in docs_dir."""
    docs = []
    for fname in os.listdir(docs_dir):
        fpath = os.path.join(docs_dir, fname)
        if fname.endswith(".txt"):
            docs.append({"source": fname, "text": _load_txt(fpath)})
        elif fname.endswith(".pdf"):
            docs.append({"source": fname, "text": _load_pdf(fpath)})
    return docs


# ── Chunking ──────────────────────────────────────────────────────────────────

def _chunk(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping fixed-size character chunks."""
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if len(c) > 50]  # drop tiny trailing fragments


# ── Index building ────────────────────────────────────────────────────────────

def init(docs_dir: str = DOCS_DIR) -> None:
    """Load docs, chunk, and build in-memory ChromaDB collection. Call once at startup."""
    global _collection

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.Client()  # in-memory; rebuilt each run

    # Drop and recreate so reloads stay clean
    try:
        client.delete_collection("farming")
    except Exception:
        pass
    _collection = client.create_collection("farming", embedding_function=embedding_fn)

    docs = _load_all_docs(docs_dir)
    ids, texts, metadatas = [], [], []

    for doc in docs:
        for i, chunk in enumerate(_chunk(doc["text"])):
            ids.append(f"{doc['source']}_{i}")
            texts.append(chunk)
            metadatas.append({"source": doc["source"]})

    if texts:
        _collection.add(documents=texts, ids=ids, metadatas=metadatas)
        print(f"[RAG] Indexed {len(texts)} chunks from {len(docs)} documents.")


# ── Retrieval ─────────────────────────────────────────────────────────────────

def retrieve(query: str, n_results: int = 2) -> str:
    """Return top-n relevant chunks as a single joined string for prompt injection."""
    if _collection is None:
        raise RuntimeError("RAG not initialised — call rag.init() first.")

    results = _collection.query(query_texts=[query], n_results=n_results)
    chunks = results["documents"][0]  # list of strings
    return "\n\n---\n\n".join(chunks)
