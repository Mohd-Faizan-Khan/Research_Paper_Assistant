import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag.llm import generate_response
from rag.context_builder import build_context


def ask(query):
    """
    Full RAG pipeline:
    query → retrieve → build context → LLM answer
    """

    print("\nBuilding context...")
    context = build_context(query)

    prompt = f"""
    You are an AI research assistant.

    Use ONLY the provided research paper abstracts.

    Rules:
    - Answer clearly and concisely
    - Cite papers like [Paper 1], [Paper 2]
    - Do NOT make up information

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    print("\nGenerating answer using phi3:mini...\n")

    return generate_response(prompt)


if __name__ == "__main__":

    query = "How do graph neural networks work?"

    answer = ask(query)

    print("\n" + "="*50)
    print("AI Answer:")
    print("="*50 + "\n")

    print(answer)