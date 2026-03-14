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
            # --- LIVE NEWS SEARCH (Behtar Filter ke sath) ---
            with st.spinner("Google se bilkul taza rates dhoond raha hoon..."):
                # Search query mein 'today' aur 'Pakistan' khud add kar raha hoon accuracy ke liye
                refined_prompt = f"{prompt} today Pakistan {aaj_ki_date}"
                search_query = DDGS().text(refined_prompt, max_results=4)
                search_data = "\n".join([r['body'] for r in search_query])

            # Groq AI Response
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""Aapka naam Gemini hai. Aap Asim Chughtai ke banaye huay AI hain. 
                        Aaj ki Date: {aaj_ki_date}. 
                        Hidayat: Sirf Internet Data se latest rates batayein. Purana data (2024/25) hargiz na dein.
                        Agar user Petrol ya Sona (Gold) ka rate puche to Roman Urdu mein bilkul fresh qeemat batayein.
                        Internet Data: {search_data}"""
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LISTEN OPTION ---
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("voice.mp3")
            st.audio("voice.mp3", format="audio/mp3")
            
        except Exception as e:
            st.error(f"Network ka masla hai. Dobara try karein. Error: {str(e)}")
