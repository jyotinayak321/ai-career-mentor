# ================================================
# vectorstore.py — FAISS Vector Store
# ================================================

import os
import pickle
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from config import settings

# Embedding model load karo
print("Loading embedding model...")
embedding_model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)
print("✅ Embedding model loaded!")

# Paths
FAISS_DIR = settings.FAISS_INDEX_PATH
INDEX_FILE = os.path.join(FAISS_DIR, "index.pkl")
DOCS_FILE = os.path.join(FAISS_DIR, "documents.pkl")


def get_embedding(text: str) -> np.ndarray:
    """Text ko vector mein convert karo"""
    return embedding_model.encode(
        text,
        convert_to_numpy=True
    )


def get_embeddings(texts: List[str]) -> np.ndarray:
    """Multiple texts ke embeddings lo"""
    return embedding_model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )


def create_vector_store(
    documents: List[str],
    metadatas: List[Dict] = None
) -> bool:
    """Documents ko FAISS mein save karo"""
    try:
        import faiss

        # Directory banao
        os.makedirs(FAISS_DIR, exist_ok=True)

        print(f"Creating embeddings for {len(documents)} documents...")

        # Embeddings banao
        embeddings = get_embeddings(documents)

        # FAISS index banao
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype(np.float32))

        print(f"✅ FAISS index created with {index.ntotal} vectors")

        # Index save karo
        with open(INDEX_FILE, "wb") as f:
            pickle.dump(index, f)

        # Documents save karo
        docs_data = {
            "documents": documents,
            "metadatas": metadatas or [{}] * len(documents)
        }
        with open(DOCS_FILE, "wb") as f:
            pickle.dump(docs_data, f)

        print("✅ Vector store saved!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def load_vector_store():
    """FAISS index load karo"""
    try:
        import faiss

        if not os.path.exists(INDEX_FILE):
            print("Vector store nahi mila!")
            return None, None

        with open(INDEX_FILE, "rb") as f:
            index = pickle.load(f)

        with open(DOCS_FILE, "rb") as f:
            docs_data = pickle.load(f)

        print(f"✅ Vector store loaded! ({index.ntotal} vectors)")
        return index, docs_data

    except Exception as e:
        print(f"Load error: {e}")
        return None, None


def search_similar(
    query: str,
    top_k: int = 3
) -> List[Dict]:
    """Query se similar documents dhundo"""
    index, docs_data = load_vector_store()

    if index is None:
        return []

    # Query embedding
    query_embedding = get_embedding(query)
    query_embedding = query_embedding.reshape(
        1, -1
    ).astype(np.float32)

    # Search karo
    distances, indices = index.search(
        query_embedding, top_k
    )

    # Results banao
    results = []
    documents = docs_data["documents"]
    metadatas = docs_data["metadatas"]

    for i, idx in enumerate(indices[0]):
        if idx < len(documents):
            results.append({
                "document": documents[idx],
                "metadata": metadatas[idx],
                "score": float(distances[0][i]),
                "rank": i + 1
            })

    return results