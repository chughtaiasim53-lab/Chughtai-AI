import streamlit as st
from groq import Groq
from gtts import gTTS
from duckduckgo_search import DDGS
import os
import base64

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
    st.info("Main Live News, Petrol/Gold rates aur Weather bata sakta hoon.")

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
            # 1. LIVE SEARCH (Keywords list ko bada kiya gaya hai)
            search_context = ""
            news_keywords = ["news", "khabar", "taza", "match", "weather", "mausam", "price", "rate", "petrol", "gold", "sona", "dollar", "currency"]
            
            if any(word in prompt.lower() for word in news_keywords):
                with st.spinner("Internet se taza rates aur news nikaal raha hoon..."):
                    # Aaj ki news aur rates dhoondna
                    search_query = f"{prompt} in Pakistan today"
                    results = DDGS().text(search_query, max_results=5)
                    search_context = "\n".join([r['body'] for r in results])

            # 2. GROQ AI RESPONSE
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain. Roman Urdu mein jawab dein. Asim ke Father: Qadir Dad, Beta: Jahandad. Agar search context diya gaya hai, to usi se latest rates batayein. Context: {search_context}"
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # 3. NATURAL VOICE (Listen Option)
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("voice.mp3")
            
            # Improved Autoplay script
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
                st.markdown(audio_html, unsafe_allow_html=True)
            
            st.audio("voice.mp3", format="audio/mp3")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
