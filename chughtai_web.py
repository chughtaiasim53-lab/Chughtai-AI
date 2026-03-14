
import streamlit as st
from openai import OpenAI

# Aapki DeepSeek API Key yahan set kar di hai
client = OpenAI(
    api_key="sk-6627f6d39cd04103bedfe8944a1d096c", 
    base_url="https://api.deepseek.com"
)

st.set_page_config(page_title="Chughtai AI (DeepSeek)", page_icon="🚀", layout="centered")

# Deep style CSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stChatInput { position: fixed; bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Chughtai AI - DeepSeek")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input aur Response
if prompt := st.chat_input("DeepSeek se kuch bhi puchein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # DeepSeek model call
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Aap ek madadgaar AI hain jiska naam Chughtai AI hai."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"DeepSeek Error: {str(e)}")
            st.info("Check karein ke aapke DeepSeek account mein balance (credits) maujood hai ya nahi.")
