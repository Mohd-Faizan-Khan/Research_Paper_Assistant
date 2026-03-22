
import numpy as np
import faiss
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def main():

    print("Loading embeddings...")

    embeddings = np.load(
        BASE_DIR/"embeddings"/"paper_embeddings.npy",
    )

    print("Embeddings shape:", embeddings.shape)


    print("Converting to float32...")

    embeddings = embeddings.astype("float32")


    dimension = embeddings.shape[1]

    print("Vector dimension:", dimension)


    print("Building FAISS index...")

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print("Total vectors in index:", index.ntotal)


    os.makedirs("vector_store", exist_ok=True)

    print("Saving FAISS index...")

    faiss.write_index(
        index,
        "vector_store/faiss_index.bin"
    )

    print("Done!")


if __name__ == "__main__":
    main()