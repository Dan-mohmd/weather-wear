import requests


def query_ollama(prompt, model="llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error: {e}"

def generate_response(prompt):
    provider = st.session_state.provider

    if provider == "Ollama":
        return query_ollama(
            prompt,
            st.session_state.ollama_model
        )
