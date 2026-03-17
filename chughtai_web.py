import streamlit as st
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# API Key - Jo aapne di thi
GOOGLE_API_KEY = "AIzaSyAajqHHlzBVwBj2QRrr1WxRYAD3lMPIOaQ"
genai.configure(api_key=GOOGLE_API_KEY)

# --- NEW MODEL CALL ---
# Hum yahan 'gemini-1.5-flash' ko simple tareeke se call kar rahe hain
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Chughtai AI")
st.markdown("**Asim Chughtai son Qadir Dad**")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan sawal likhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Simple response call
            response = model.generate_content(f"Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error Detail: {e}")
