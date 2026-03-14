import streamlit as st
from groq import Groq

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

# Welcome message agar chat khali ho
if not st.session_state.messages:
    st.markdown("### Hello, Asim Chughtai")
    st.info("Main aapka personal AI dost hoon. Aap mujhse kheti baari ya family ke bare mein kuch bhi puch sakte hain.")

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
            # AI ki Personality (The Brain)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """
                        Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain.
                        Aap dosti se, aqalmandana aur Roman Urdu mein jawab dete hain.
                        Asim ki details:
                        - Father: Qadir Dad Chughtai (DSR Rangers).
                        - Beta: Jahandad (4 saal ka).
                        - Location: Basti Ahmadabad, Rahim Yar Khan.
                        - Farming: 2.5 acre farm (Lahsun, Aam, Mung phali).
                        Asim ke doston ki tarah baat karein aur unhein behtareen mashwaray dein.
                        """
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {str(e)}")from gtts import gTTS
import os

# ... (baaki purana code) ...

if response:
    st.markdown(response.text)
    
    # Audio banane ka tareeka
    tts = gTTS(text=response.text, lang='ur') # Urdu ke liye 'ur'
    tts.save("speech.mp3")
    st.audio("speech.mp3") # Audio player screen par dikhaye
