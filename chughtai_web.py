import streamlit as st
from groq import Groq
from gtts import gTTS
from duckduckgo_search import DDGS # Live News ke liye
import os

# Groq API Key
client = Groq(api_key="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")

# Page Layout
st.set_page_config(page_title="Chughtai AI", page_icon="✨", layout="centered")

# Gemini Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    h1 { color: #ffffff; font-family: 'Google Sans', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Chughtai AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.markdown("### Hello,")
    st.info("Main aapka personal AI dost hoon. Aap mujhse Live News, kheti baari ya family ke bare mein kuch bhi puch sakte hain.")

# Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Yahan kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # --- LIVE NEWS SEARCH (Internet Se Data Lena) ---
            with st.spinner("Internet par taza khabrein dhoond raha hoon..."):
                search_query = DDGS().text(prompt, max_results=3)
                search_data = "\n".join([r['body'] for r in search_query])

            # Groq AI Response with Search Data
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain. Roman Urdu mein jawab dein. Internet Data: {search_data}. Asim ke Father: Qadir Dad, Beta: Jahandad."
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LISTEN OPTION (Audio Generator) ---
            # 'hi' (Hindi) voice Urdu ke liye zyada natural/insaani lagti hai
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("voice.mp3")
            st.audio("voice.mp3", format="audio/mp3")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
