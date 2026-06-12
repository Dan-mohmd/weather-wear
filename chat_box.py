import streamlit as st


def render_chat_box(ask_ollama, ask_gemini, ask_openai):
    st.markdown("""
    <style>
    .st-key-mobile_chat_box {
        position: fixed;
        right: 24px;
        bottom: 24px;
        width: 390px;
        height: 640px;
        z-index: 9999;
        background: #0e1117;
        border: 1px solid #30363d;
        border-radius: 18px;
        padding: 16px;
        overflow-y: auto;
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
    }

    @media (max-width: 520px) {
        .st-key-mobile_chat_box {
            right: 10px;
            left: 10px;
            bottom: 10px;
            width: auto;
            height: 85vh;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.get("chat_open", False):
        return

    with st.container(border=True, key="mobile_chat_box"):
        top1, top2 = st.columns([8, 1])

        with top1:
            st.markdown("### AI Assistant")

        with top2:
            if st.button("✕", key="close_chat"):
                st.session_state.chat_open = False
                st.rerun()

        provider = st.selectbox(
            "Provider",
            ["Ollama", "Gemini", "OpenAI"],
            key="provider"
        )

        if provider == "Ollama":
            st.text_input("Model", "llama3", key="ollama_model")
        elif provider == "Gemini":
            st.text_input("Gemini Key", type="password", key="api_key")
        else:
            st.text_input("OpenAI Key", type="password", key="api_key")

        st.divider()

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask anything...")

        if prompt:
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.spinner("Thinking..."):
                if provider == "Ollama":
                    answer = ask_ollama(prompt, st.session_state.ollama_model)
                elif provider == "Gemini":
                    answer = ask_gemini(prompt, st.session_state.api_key)
                else:
                    answer = ask_openai(prompt, st.session_state.api_key)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()