import streamlit as st
import google.generativeai as genai

# Aapki nayi API Key yahan set kar di hai
genai.configure(api_key="AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE")

# Stable model istemal kar rahe hain
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Chughtai AI", page_icon="✨", layout="centered")

# Gemini style UI
st.markdown("""
    <style>
    .main { background-color: #131314; }
    .stChatInput { position: fixed; bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Header
if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; color: white;'>Hello, Asim Chughtai</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Main aapki kaise madad kar sakta hoon?</p>", unsafe_allow_html=True)

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input aur Response
if prompt := st.chat_input("Yahan kuch bhi search karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar koi masla aaye to asli wajah bataye
            st.error(f"Masla: {str(e)}")
