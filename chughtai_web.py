import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- Setup ---
# Yahan apni Groq Key lazmi dalein
client = Groq(api_key="gsk_YAHAN_APNI_GROQ_KEY_DALEIN")

st.set_page_config(page_title="Chughtai Human AI", page_icon="🎙️", layout="centered")

# Styling taaki interface pyara lage
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Chughtai Human-Voice AI")
st.info("Main Groq ki madad se bijli ki tarah tez jawab deta hoon aur bolta bhi hoon!")

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input aur Response ---
if prompt := st.chat_input("Puchiye, main bol kar jawab doon ga..."):
    # User ka message save karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 1. Groq se Fast Response (Context ke sath)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            ai_text = completion.choices[0].message.content
            st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})

            # 2. Voice (Audio Generation)
            tts = gTTS(text=ai_text, lang='hi', slow=False) 
            audio_file = "response.mp3"
            tts.save(audio_file)
            
            # 3. Auto-play Logic
            with open(audio_file, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                audio_html = f"""
                    <audio autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(audio_html, unsafe_allow_html=True)
            
            st.audio(audio_file) # Manual player
            
        except Exception as e:
            st.error(f"Masla: {str(e)}")
