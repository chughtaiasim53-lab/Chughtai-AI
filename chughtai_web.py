import streamlit as st
from groq import Groq
from gtts import gTTS
from duckduckgo_search import DDGS 
import os
import datetime

# Groq API Key
client = Groq(api_key="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")

# Page Layout
st.set_page_config(page_title="Chughtai AI Live 2026", page_icon="✨", layout="centered")

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
    st.info(f"Assalam-o-Alaikum Asim! Aaj {aaj_ki_date} hai. Main Gold, Petrol aur Live News bilkul sahi bata sakta hoon.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Petrol rate ya Gold price puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Internet se bilkul taza (March 2026) data scan ho raha hai..."):
                # Behtar search query: Specific sites aur Date force karna
                refined_prompt = f"{prompt} rate in Pakistan today {aaj_ki_date} live UrduPoint Hamariweb"
                
                search_data = ""
                with DDGS() as ddgs:
                    # News aur Text dono scan karna behtar results deta hai
                    search_query = [r for r in ddgs.text(refined_prompt, max_results=6)]
                    search_data = "\n".join([f"Content: {r['body']}" for r in search_query])

            # Groq AI Response
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain. 
                        Aaj ki Date: {aaj_ki_date}. 
                        
                        ROLE: Aap ek news reporter hain. 
                        DATA: {search_data}
                        
                        RULES:
                        1. Is data mein se sirf March 2026 ke rates batayein. 
                        2. Agar data purana hai (2024/2025), to saaf keh dein ke 'Taza rate abhi update nahi hua'. 
                        3. Jawab Roman Urdu mein dein aur rates ko bold (**) likhein.
                        4. Petrol aur Gold ke liye sirf authenticated sources ka data uthayein."""
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LISTEN OPTION (Voice) ---
            # Urdu Voice ke liye 'hi' (Hindi) ya 'ur' behtar hai
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("voice.mp3")
            st.audio("voice.mp3", format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error(f"Network ka masla hai ya API limit khatam ho gayi hai. Error: {str(e)}")
