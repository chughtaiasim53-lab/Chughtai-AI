import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
# Aapki Key: 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
client = Groq(api_key="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")

# --- Interface Design (Beauty + Gemini Look) ---
st.set_page_config(page_title="Chughtai Gemini-AI v2", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stChatInputContainer { border-radius: 20px !important; border: 2px solid #4facfe !important; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 15px; border-left: 5px solid #4facfe; }
    h1 { background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Chughtai Super-Accurate AI")

# Aaj ki Date
aaj = datetime.date.today().strftime("%d %B %Y")
st.write(f"📅 Aaj ki Date: **{aaj}** | Status: **High Accuracy Mode**")

# System ki sakht hidayat
system_rules = f"""
Aap ek High-Accuracy Assistant hain. Aaj {aaj} hai.
1. User (Asim Chughtai) ko hamesha 100% sahi rates batane hain.
2. Agar internet par purana data miley, to user ko batayein ke 'Mujhe abhi live rate nahi mila'.
3. Petrol aur Gold ke rates ke liye sirf 2026 ki news par yaqeen karein.
4. Jawab Roman Urdu mein dein aur ahem maloomat ko Bold karein.
5. User ki ghalat baat par 'Theek hai' mat kahein, usay sahi data dikhayein.
"""

if prompt := st.chat_input("Sona, Petrol ya mandi ke rates puchiye..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Accuracy check ho raha hai..."):
                # 1. LIVE WEB SEARCH
                with DDGS() as ddgs:
                    # Sirf sabse taza results dhoondne ke liye query
                    search_query = f"{prompt} Pakistan latest official rate today {aaj} news"
                    results = [r for r in ddgs.text(search_query, max_results=3)]
                    live_context = "\n".join([f"Live News: {r['body']}" for r in results])

            # 2. ACCURATE PROCESSING (Temperature 0 means NO GUESSING)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"{system_rules}\nWeb Data: {live_context}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0  # Is se AI ghalat tukkay nahi marega
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)

            # 3. VOICE
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"System Error: {str(e)}")
