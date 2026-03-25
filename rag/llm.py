import ollama

MODEL_NAME = "phi3:mini"

def generate_response(prompt):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']

    except Exception as e:
        return f"Error: {str(e)}"