import streamlit as st
import google.generativeai as genai

# Aapki API Key
genai.configure(api_key="AIzaSyBCvOiIEuU7mWsqTCBddevX2on2xQqmucE")

# 400 error se bachne ke liye sabse stable model
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("✨ Chughtai AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Simple content generation
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Technical Error: {str(e)}")
