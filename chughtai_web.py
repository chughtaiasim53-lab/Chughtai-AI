import streamlit as st
import google.generativeai as genai

# Setup
genai.configure(api_key="AIzaSyD-Msv12DuyRdKH6yG_BOep9_lT4pha4sk")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Chughtai AI", page_icon="✨", layout="centered")

# CSS for Gemini Look
st.markdown("""
    <style>
    .main { background-color: #131314; }
    h1 { color: #e3e3e3; font-family: 'Google Sans', sans-serif; text-align: center; margin-top: 15%; }
    .stChatInput { position: fixed; bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# User ka naam store karna
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Agar naam nahi pata to pehle naam puchein
if not st.session_state.user_name:
    st.markdown("<h1>Welcome to Chughtai AI</h1>")
    name_input = st.text_input("Apna naam likhein shuru karne ke liye:", key="name_box")
    if name_input:
        st.session_state.user_name = name_input
        st.rerun()
else:
    # Jab naam mil jaye to Gemini jaisa interface
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.markdown(f"<h1>Hello, {st.session_state.user_name}</h1>")
        st.markdown("<p style='text-align: center; color: #888;'>Main aapki kaise madad kar sakta hoon?</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Yahan kuch bhi search karein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Masla aaya: {e}")
