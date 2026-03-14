import streamlit as st
from groq import Groq

# Aapki Groq API Key yahan set kar di hai
client = Groq(api_key="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")

st.set_page_config(page_title="Chughtai AI", page_icon="⚡", layout="centered")

# Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0f1115; color: white; }
    .stChatInput { position: fixed; bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Chughtai AI (Super Fast)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Yahan kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llama 3.3 model jo sabse naya aur fast hai
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Aapka naam Chughtai AI hai. Aap Asim Chughtai ke banaye huay ek madadgaar assistant hain. Hamesha Urdu ya Roman Urdu mein jawab dein."},
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Technical Error: {str(e)}")
