import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .gemini-title { font-family: 'Google Sans'; font-size: 40px; text-align: center; background: linear-gradient(to right, #4285f4, #9b72cb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stChatInputContainer { border-radius: 30px !important; }
    /* Sidebar style for History */
    .css-1639116 { background-color: #1e1f20 !important; } 
    </style>
    """, unsafe_allow_html=True)

# --- HISTORY LOGIC ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar mein History dikhana
with st.sidebar:
    st.title("📜 Chat History")
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        st.info(f"{chat['user'][:30]}...")

# --- MAIN INTERFACE ---
st.markdown('<h1 class="gemini-title">Chughtai AI Super Pro</h1>', unsafe_allow_html=True)

# Chat Display
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["bot"])

# --- INPUT & SEARCH ---
if prompt := st.chat_input("Sawal puchiye..."):
    # User message display
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching..."):
                with DDGS() as ddgs:
                    r = [res for res in ddgs.text(f"{prompt} Pakistan 2026", max_results=2)]
                    context = "\n".join([res['body'] for res in r])
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            
            # Save to History
            st.session_state.chat_history.append({"user": prompt, "bot": ans})
            
            # --- AUDIO LOGIC (No Autoplay) ---
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                # Autoplay="false" taaki sirf click par chalay
                st.markdown(f'**Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls autoplay="false"></audio>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
