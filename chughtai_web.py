import streamlit as st
from groq import Groq

# --- Setup ---
# Aapki provide ki gayi Groq API Key
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="✨", layout="centered")

# --- CSS for Gemini Dark Look ---
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    h1 { color: #e3e3e3; font-family: 'Google Sans', sans-serif; text-align: center; }
    .stChatInput { position: fixed; bottom: 3rem; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# User ka naam store karna
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Agar naam nahi pata to pehle naam puchein
if not st.session_state.user_name:
    st.markdown("<br><br><br><h1>Welcome to Chughtai AI</h1>", unsafe_allow_html=True)
    name_input = st.text_input("Apna naam likhein shuru karne ke liye:", key="name_box")
    if name_input:
        st.session_state.user_name = name_input
        st.rerun()
else:
    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome Message (Sirf shuru mein dikhega)
    if len(st.session_state.messages) == 0:
        st.markdown(f"<br><br><h1>Hello, {st.session_state.user_name}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Main Chughtai AI hoon, aapki kaise madad kar sakta hoon?</p>", unsafe_allow_html=True)

    # Purani chat dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Yahan kuch bhi poochein..."):
        # User ka msg dikhana
        st
