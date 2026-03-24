import os
import sys
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Paths
INDEX_PATH = "vector_store/faiss_index.bin"
METADATA_PATH = "embeddings/paper_metadata.pkl"


# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)


# Load metadata
print("Loading metadata...")
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)


def search(query, k=5):
    """
    Search similar papers using semantic search
    """

    print(f"\nQuery: {query}")

    # Embed query
    query_embedding = model.encode([query])

    # Convert to float32
    query_embedding = np.array(query_embedding).astype("float32")

    # Search
    distances, indices = index.search(query_embedding, k)

    results = []

    for i, idx in enumerate(indices[0]):
        paper = metadata[idx]

        results.append({
            "title": paper["title"],
            "abstract": paper["abstract"],
            "pdf_url": paper["pdf_url"],
            "score": float(distances[0][i])
        })

    return results


if __name__ == "__main__":

    query = "graph neural networks"

    results = search(query)

    print("\nTop Results:\n")

    for i, res in enumerate(results, 1):
        print(f"{i}. {res['title']}")
        print(f"Score: {res['score']}")
        print(f"PDF: {res['pdf_url']}")
        print()