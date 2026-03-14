import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI SETTINGS ---
st.set_page_config(page_title="Chughtai AI Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .gemini-title { font-size: 40px; text-align: center; color: #4285f4; font-family: 'Google Sans'; }
    /* Sidebar History Style */
    section[data-testid="stSidebar"] { background-color: #1e1f20 !important; width: 300px !important; }
    .history-item { padding: 10px; border-bottom: 1px solid #333; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (History & Audio) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR (History Display) ---
with st.sidebar:
    st.markdown("### 📜 Chat History")
    if st.button("🗑️ Clear All"):
        st.session_state.chat_history = []
        st.rerun()
    
    # History ko list ki tarah dikhana
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"<div class='history-item'><b>You:</b> {chat['user'][:40]}...</div>", unsafe_allow_html=True)

# --- MAIN SCREEN ---
st.markdown('<h1 class="gemini-title">✨ Chughtai AI Pro</h1>', unsafe_allow_html=True)

# Purani chats screen par dikhana
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["bot"])

# --- INPUT BOX ---
if prompt := st.chat_input("Sawal yahan likhein..."):
    # User message
    st.session_state.chat_history.append({"user": prompt, "bot": "Thinking..."})
    st.rerun()

# Processing the last message
if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Thinking...":
    last_prompt = st.session_state.chat_history[-1]["user"]
    
    try:
        with st.spinner("Searching..."):
            with DDGS() as ddgs:
                r = [res for res in ddgs.text(f"{last_prompt} Pakistan 2026", max_results=2)]
                context = "\n".join([res['body'] for res in r])
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                {"role": "user", "content": last_prompt}
            ],
            temperature=0
        )
        ans = completion.choices[0].message.content
        
        # Update History with actual answer
        st.session_state.chat_history[-1]["bot"] = ans
        
        # Audio Create (But NO Auto-Play)
        tts = gTTS(text=ans, lang='hi')
        tts.save("v.mp3")
        with open("v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.session_state.audio_html = f'<audio src="data:audio/mp3;base64,{b64}" controls></audio>'
        
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Audio Player display (Only if exists)
if "audio_html" in st.session_state:
    st.markdown("### 🔊 Jawab Suniye:")
    st.markdown(st.session_state.audio_html, unsafe_allow_html=True)
    # Audio dikhane ke baad state se delete kar dein taaki agli baar khud na chalay
    del st.session_state.audio_html
