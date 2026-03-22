import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "data" / "raw" / "papers_raw.json"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "papers_clean.csv"


def load_data():
    with open(INPUT_DIR, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def clean_text(text):
    if not text:
        return ""

    text = text.strip()
    text = " ".join(text.split())
    return text

def processed_papers(papers):
    cleaned_papers = []

    for paper in papers:
        title = clean_text(paper.get("title", ""))
        abstract = clean_text(paper.get("abstract", ""))

        if not abstract:
            continue

        year = paper.get("published", "")[:4]

        cleaned_papers.append({
            "title": title,
            "abstract": abstract,
            "authors": ", ".join(paper.get("authors", [])),
            "year": year,
            "category": ", ".join(paper.get("categories", [])),
            "pdf_url": paper.get("pdf_url", ""),
        })

    return cleaned_papers

def remove_duplicates(df):
    df = df.drop_duplicates(subset=["title"])
    return df

if __name__ == "__main__":
    print("Loading raw papers...")
    papers = load_data()

    print(f"Loaded {len(papers)} papers")

    print("Cleaning papers...")
    cleaned = processed_papers(papers)

    df = pd.DataFrame(cleaned)

    print("Removing duplicates...")
    df = remove_duplicates(df)

    print(f"Final dataset size: {len(df)}")

    print("Saving cleaned dataset...")
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved to {OUTPUT_FILE}")