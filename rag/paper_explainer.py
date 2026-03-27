import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.llm import generate_response
from retrieval.semantic_search import search


def explain_paper(title, abstract):
    """
    Explain research paper in simple terms
    """

    prompt = f"""
    You are an AI research assistant.

    Explain the following research paper in simple terms.

    Paper Title:
    {title}

    Abstract:
    {abstract}

    Explain in this format:

    Key Idea:
    Why It Matters:
    Simple Example:
    """

    return generate_response(prompt)


if __name__ == "__main__":

    query = "graph neural networks"

    results = search(query)

    paper = results[0]

    explanation = explain_paper(
        paper["title"],
        paper["abstract"]
    )

    print("\nTitle:\n", paper["title"])
    print("\nExplanation:\n")
    print(explanation)