import sys
import os

#Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.llm import generate_response

print(generate_response("Explain transformer model of ML in 2 lines"))