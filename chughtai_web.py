import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import os
import time
from PIL import Image
import io
import streamlit.components.v1 as components

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE (Gemini Dark Theme) ---
st.set_page_config(page_title="Chughtai AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Round Elements */
    .card { background-color: #1e1f20; padding: 20px; border-radius: 25px; border: 1px solid #333; margin-bottom: 20px; }
    [data-testid="stChatMessage"] { border-radius: 25px; padding: 15px; margin-bottom: 10px; background-color: #1e1f20; border: 1px solid #333; }
    
    /* Search Status Design (Niche wala) */
    .search-status { color: #4facfe; font-size: 14px; font-style: italic; margin-bottom: 10px; margin-left: 10px; }
    
    /* Round Inputs */
    .stChatInputContainer textarea { border-radius: 30px !important; border: 1px solid #4facfe !important; padding: 10px 20px !important; }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTO SCROLL SCRIPT ---
def scroll_down():
    components.html(
        """
        <script>
            var mainContainer = window.parent.document.querySelector('section.main');
            if (mainContainer) {
                mainContainer.scrollTo({ top: mainContainer.scrollHeight, behavior: 'smooth' });
            }
        </script>
        """,
        height=0,
    )

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN SCREEN ---
tab1, tab2, tab3 = st.tabs(["💬 Gemini Chat", "🚜 Agri Plan", "🏠 Build Plan"])

# --- TAB 1: SMART CHAT & VISION ---
with tab1:
    # History Display
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Search Indicator Placeholder (Niche ke liye)
    status_placeholder = st.empty()

    # Input Box
    if prompt := st.chat_input("Yahan sawal puchiye..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        # Searching start (Niche nazar ayega)
        status_placeholder.markdown('<p class="search-status">🔍 Maloomat talash ki ja rahi hain...</p>', unsafe_allow_html=True)
        
        # Search Logic
        search_data = ""
        try:
            with DDGS() as ddgs:
                r = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                search_data = "\n".join([i['body'] for i in r])
        except: pass

        # AI Response
        with st.chat_message("assistant"):
            # Jaise hi AI shuru ho, searching status gayab kar do
            status_placeholder.empty()
            
            response_area = st.empty()
            full_ans = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": f"Context: {search_data}\n\nQ: {prompt}"}]
            )
            ans_text = completion.choices[0].message.content
            
            # Streaming + Auto Scroll
            for chunk in ans_text.split():
                full_ans += chunk + " "
                response_area.markdown(full_ans + "▌")
                scroll_down()
                time.sleep(0.05)
            response_area.markdown(full_ans)
            
            st.session_state.history.append({"u": prompt, "b": full_ans})
            
            # Voice Output
            try:
                tts = gTTS(text=full_ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- TAB 2 & 3 (Same as before) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Agri Management</h3>", unsafe_allow_html=True)
    # Fasal logic...
