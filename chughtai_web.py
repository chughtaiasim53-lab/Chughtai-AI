import streamlit as st
import google.generativeai as genai

# Nayi API Key yahan dhyan se paste karein
API_KEY = "YAHAN_APNI_NAYI_KEY_PASTE_KAREIN"

genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Chughtai AI", page_icon="✨")

# Interface setup
st.title("Chughtai AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sawal puchein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Hum 1.5-flash use karenge jo fast hai
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Google ne khali jawab bheja hai.")
        except Exception as e:
            # Ye line humein asli masla batayegi
            st.error(f"Error Message: {str(e)}")
