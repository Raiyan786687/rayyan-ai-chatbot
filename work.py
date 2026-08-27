import streamlit as st
import requests
import time

# Session state initialize
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Credentials
TARGET_EMAIL = "rayyan@gmail.com"
TARGET_PASSWORD = "(Rayyan.786687)"

# OpenRouter API Setup
OPENROUTER_API_KEY = "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"  # <-- Apni API Key yahan paste karein

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

    # Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if user_query := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # AI API Call
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
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "Rayyan AI Assistant"
                }

                # High Reliability Request Loop
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
                            timeout=30  # Timeout badha diya hai taakay slow responses na cut hon
                        )
                        if response.status_code == 200:
                            data = response.json()
                            if "choices" in data and len(data["choices"]) > 0:
                                ai_reply = data["choices"][0]["message"]["content"]
                                if ai_reply:
                                    break
                    except Exception:
                        continue

                if ai_reply:
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                else:
                    st.warning("Server par traffic zyaada hai, kripya apna sawal dobara bhejain.")
