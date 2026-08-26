import streamlit as st
import requests
import json

# Page Config
st.set_page_config(page_title="Rayyan Agentic Chatbot", page_icon="🤖")

# Session state initialize karein
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Login Credentials
TARGET_EMAIL = "rayyan@gmail.com"
TARGET_PASSWORD = "Password123"

# OpenRouter API Setup (Yahan apni API Key dalein)
OPENROUTER_API_KEY = "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"

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 Login to Access Chatbot")
    
    user_email = st.text_input("Enter Email")
    user_pass = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if user_email.strip().lower() == TARGET_EMAIL.lower() and user_pass.strip() == TARGET_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Galat Email ya Password!")

# --- MAIN CHATBOT SCREEN ---
else:
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🤖 Rayyan Agentic Chatbot")
    st.success("Mubarak ho! Login successfully ho gaya hai.")

    # Show Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Question Input Box
    if user_input := st.chat_input("Poochhein apna sawal..."):
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call OpenRouter API
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                try:
                    headers = {
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "openai/gpt-3.5-turbo", # Ya apna preferred OpenRouter model
                        "messages": st.session_state.messages
                    }
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        data=json.dumps(payload)
                    )
                    
                    if response.status_code == 200:
                        bot_reply = response.json()['choices'][0]['message']['content']
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        st.error("API Key check karein ya OpenRouter server busy hai.")
                except Exception as e:
                    st.error(f"Error: {e}")