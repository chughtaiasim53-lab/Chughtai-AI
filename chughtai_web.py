import streamlit as st
import google.generativeai as genai
import os

# API Key को सुरक्षित रूप से Secrets से लेना
# GitHub/Streamlit Cloud पर इसे 'Settings' में सेट करें
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDJFGXd4A3xwJr949691pivVrod6BE5K4M")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Chughtai AI", page_icon="🤖")
st.title("🤖 Chughtai AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chughtai AI से पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Technical error! अपनी API Key चेक करें।")
