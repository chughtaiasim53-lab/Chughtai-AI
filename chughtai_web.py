import streamlit as st
import os
import base64
from PIL import Image
from gtts import gTTS
from engine import get_chughtai_response

# 1. Gemini Style Layout
st.set_page_config(page_title="Chughtai AI", page_icon="🦁", layout="wide")

# Custom CSS for Gemini Look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar with History
with st.sidebar:
    st.title("🦁 Chughtai AI")
    st.subheader("Next-Gen Assistant")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.write("🕒 Recent Activity")
    st.caption("No recent chats")

# 3. Chat Session Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Image Uploader (For Face Analysis)
uploaded_file = st.sidebar.file_uploader("Upload Image for Analysis", type=["jpg", "png", "jpeg"])

# 5. Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("Ask Chughtai AI..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            img = Image.open(uploaded_file) if uploaded_file else None
            response_text = get_chughtai_response(prompt, img)
            st.markdown(response_text)
            
            # Voice Output
            tts = gTTS(text=response_text[:200], lang='ur') # Limit for speed
            tts.save("speech.mp3")
            with open("speech.mp3", "rb") as f:
                data = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay="true">', unsafe_allow_html=True)
            os.remove("speech.mp3")

    st.session_state.messages.append({"role": "assistant", "content": response_text})
