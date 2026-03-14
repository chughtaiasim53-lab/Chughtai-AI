import streamlit as st
import google.generativeai as genai

# Aapki API Key
API_KEY = "AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Chughtai AI", page_icon="✨")

# Sabse stable aur purana naam jo 404 nahi deta
model = genai.GenerativeModel('gemini-pro')

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
            # Response generate karna
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar abhi bhi masla aaye to asli wajah yahan nazar aayegi
            st.error(f"Technical Error: {str(e)}")
