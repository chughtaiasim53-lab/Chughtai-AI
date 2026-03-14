import streamlit as st
import google.generativeai as genai

# Setup API Key
genai.configure(api_key="AIzaSyAn0IvcL2ja2oc8saRKNsFoxODO15tfcO0")

# Ye tareeka har model ko 404 se bachata hai
model = genai.GenerativeModel('gemini-pro') 

st.set_page_config(page_title="Chughtai AI", page_icon="✨", layout="centered")

# Gemini Look CSS
st.markdown("""
    <style>
    .main { background-color: #131314; }
    .stChatInput { position: fixed; bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; color: white;'>Hello, Asim Chughtai</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Main aapki kaise madad kar sakta hoon?</p>", unsafe_allow_html=True)

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Yahan kuch bhi search karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Response generate karna
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar phir bhi error aaye to ye chota msg dikhaye
            st.error("Google Server Busy hai, 30 seconds baad 'Hi' likhein.")

            
