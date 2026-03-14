import streamlit as st
from groq import Groq
from gtts import gTTS
from duckduckgo_search import DDGS 
import os
import datetime

# Groq API Key
client = Groq(api_key="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")

# Page Layout
st.set_page_config(page_title="Chughtai AI Live", page_icon="✨", layout="centered")

# Aaj ki date
aaj_ki_date = datetime.date.today().strftime("%d %B %Y")

# Gemini Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { color: #ffffff; font-family: 'Google Sans', sans-serif; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Chughtai Live AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.info(f"Assalam-o-Alaikum Asim! Aaj {aaj_ki_date} hai. Main Live News aur Rates bata sakta hoon.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Petrol rate ya Gold price puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Internet se bilkul taza data scan ho raha hai..."):
                # Behtar search query taaki purana data na aaye
                refined_prompt = f"latest {prompt} in Pakistan {aaj_ki_date} news"
                with DDGS() as ddgs:
                    search_query = [r for r in ddgs.text(refined_prompt, max_results=5)]
                    search_data = "\n".join([f"Source: {r['href']} - Content: {r['body']}" for r in search_query])

            # Groq AI Response
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain. 
                        Aaj ki Date: {aaj_ki_date}. 
                        IMPORTANT: Niche diye gaye search data ko ghaur se parhein. 
                        Ismein jo sabse LATEST rate hai (March 2026 ka), sirf wo batayein. 
                        Agar data mein 2024 ya 2025 likha hai to usay ignore karein. 
                        User ko Roman Urdu mein jawab dein.
                        
                        Internet Search Data:
                        {search_data}"""
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LISTEN OPTION (Auto-Play) ---
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("voice.mp3")
            st.audio("voice.mp3", format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error(f"Network ka masla hai. Error: {str(e)}")
