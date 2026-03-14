import streamlit as st
import google.generativeai as genai

# Sahi API Key
genai.configure(api_key="AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE")

# Stable model jo 404 nahi dega
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
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Masla: {str(e)}")
