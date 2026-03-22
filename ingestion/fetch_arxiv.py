import arxiv
import json
from pathlib import Path
from tqdm import tqdm

# Creating o/p directory, root path and o/p file

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_PATH / "papers_raw.json"

#arXiv search function

def fetch_arxiv_papers(
    query="""
    (cat:cs.AI OR cat:cs.LG OR stat.ML)
    AND (transformer OR "large language model" OR diffusion OR "graph neural network" OR "reinforcement learning")
    """, max_results=10000
):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
    )

    papers = []

    client = arxiv.Client()
    for result in tqdm(client.results(search), total=max_results):
        paper = {
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "categories": result.categories,
            "published": result.published.isoformat(),
            "pdf_url": result.pdf_url
        }

        papers.append(paper)

    return papers


def save_papers(papers):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)


if __name__ == "__main__":
    print("Fetching papers from arXiv...")

    papers = fetch_arxiv_papers()

    print(f"Fetched {len(papers)} papers")

    print("Saving to file...")
    save_papers(papers)

    print(f"Saved to {OUTPUT_FILE}")