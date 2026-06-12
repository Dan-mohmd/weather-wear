import requests
from openai import OpenAI


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


def query_openai(prompt, api_key):
    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


def generate_response(prompt):
    provider = st.session_state.provider

    if provider == "Ollama":
        return query_ollama(
            prompt,
            st.session_state.ollama_model
        )

    return query_openai(
        prompt,
        st.session_state.api_key
    )