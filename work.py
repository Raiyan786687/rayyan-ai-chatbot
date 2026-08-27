import streamlit as st

# Session state initialize karein
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Aapke fixed credentials
TARGET_EMAIL = "rayyan@gmail.com"
TARGET_PASSWORD = "Rayyan786687##"

if not st.session_state.logged_in:
    st.title("🔐 Login to Access Chatbot")
    
    # Inputs
    user_email = st.text_input("Enter Email", key="e_input")
    user_pass = st.text_input("Enter Password", type="password", key="p_input")

    if st.button("Login"):
        # Match check karna
        if user_email.strip() == TARGET_EMAIL and user_pass.strip() == TARGET_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Galat Email ya Password!")

else:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🤖 Rayyan Agentic Chatbot")
    st.success("Mubarak ho! Login successfully ho gaya hai.")

    # ==========================================
    # AAPKA MAIN CHATBOT CODE YAHAN AAYEGA
    # ==========================================
