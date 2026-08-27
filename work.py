import streamlit as st
import requests

# Session state initialize karein
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Credentials
TARGET_EMAIL = "rayyan@gmail.com"
TARGET_PASSWORD = "(Rayyan.786687)"  # <-- Apna secret password daalein

# OpenRouter API Setup
OPENROUTER_API_KEY = "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"   # <-- Yahan apni OpenRouter API Key paste karein

if not st.session_state.logged_in:
    st.title("🔐 Login to Access Chatbot")
    
    user_email = st.text_input("Enter Email", key="e_input")
    user_pass = st.text_input("Enter Password", type="password", key="p_input")

    if st.button("Login"):
        if user_email.strip() == TARGET_EMAIL and user_pass.strip() == TARGET_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Galat Email ya Password!")

else:
    # Logout Button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.rerun()

    st.title("🤖 Rayyan Agentic AI Assistant")
    st.write("Welcome! Ask me anything below.")

    # Previous Chat History Show Karna
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input Box
    if user_query := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # AI API Call with Automatic Fallback Models (No Errors for Clients)
        with st.chat_message("assistant"):
            with st.spinner("AI reply soch raha hai..."):
                FREE_MODELS = [
                    "google/gemini-2.0-flash-exp:free",
                    "meta-llama/llama-3.3-70b-instruct:free",
                    "qwen/qwen-2.5-coder-32b-instruct:free",
                    "deepseek/deepseek-r1:free"
                ]
                
                ai_reply = None
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                }

                for model in FREE_MODELS:
                    try:
                        payload = {
                            "model": model,
                            "messages": [
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ]
                        }
                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=15
                        )
                        if response.status_code == 200:
                            ai_reply = response.json()["choices"][0]["message"]["content"]
                            break
                    except Exception:
                        continue

                if ai_reply:
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                else:
                    st.error("Server busy hai. Kripya thodi der baad dobara try karein.")
