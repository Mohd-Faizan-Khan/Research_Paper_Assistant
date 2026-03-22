import pandas as pd
import numpy as np
import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "processed" / "papers_clean.csv"

def main():

    print("Loading cleaned dataset...")

    # load cleaned papers
    df = pd.read_csv(INPUT_FILE)

    print(f"Number of papers: {len(df)}")


    print("Combining title and abstract...")

    # combine title + abstract
    texts = (
        df["title"] + ". " + df["abstract"]
    ).tolist()


    print("Loading embedding model...")

    # load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")


    print("Generating embeddings...")

    # generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32
    )


    print("Saving embeddings...")

    # save embeddings
    np.save(
        "embeddings/paper_embeddings.npy",
        embeddings
    )


    print("Saving metadata...")

    # save metadata
    metadata = df.to_dict("records")

    with open(
        "embeddings/paper_metadata.pkl",
        "wb"
    ) as f:
        pickle.dump(metadata, f)


    print("Embeddings shape:", embeddings.shape)
    print("Done!")

if __name__ == "__main__":
    main()