import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from retrieval.semantic_search import search


def build_context(query, k=3):
    """
    Build LLM context from retrieved papers
    """

    results = search(query, k)

    context = ""

    for i, paper in enumerate(results, 1):
        context += f"""
        Paper {i}
        Title: {paper['title']}

        Abstract:
        {paper['abstract'][:150]}

        Source: {paper['pdf_url']}
        ---------------------
        """

    return context,results


if __name__ == "__main__":

    query = "graph neural networks"

    context = build_context(query)

    print("\nGenerated Context:\n")
    print(context)