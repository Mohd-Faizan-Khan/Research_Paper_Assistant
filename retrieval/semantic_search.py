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


# Lazy loaded globals
model = None
index = None
metadata = None


def load_model():
    global model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            local_files_only=True
        )
    return model


def load_index():
    global index
    if index is None:
        print("Loading FAISS index...")
        index = faiss.read_index(INDEX_PATH)
    return index


def load_metadata():
    global metadata
    if metadata is None:
        print("Loading metadata...")
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)
    return metadata


def search(query, k=3):
    """
    Search similar papers using semantic search
    """

    model = load_model()
    index = load_index()
    metadata = load_metadata()

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
            "score": round(float(distances[0][i]), 4)
        })

    return results


if __name__ == "__main__":

    test_queries = [
        "graph neural networks",
        "vision transformers",
        "diffusion models",
        "reinforcement learning"
    ]

    for query in test_queries:
        print(f"\n{'=' * 50}")
        print(f"Query: {query}")
        print(f"{'=' * 50}")

        results = search(query)

        for i, res in enumerate(results, 1):
            print(f"\n{i}. {res['title']}")
            print(f"Score: {res['score']}")
            print(f"Abstract: {res['abstract']}")
            print(f"PDF: {res['pdf_url']}")