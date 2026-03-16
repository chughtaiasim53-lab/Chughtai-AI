import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import os
import time
import streamlit.components.v1 as components

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE (Gemini Pro Layout) ---
st.set_page_config(page_title="Chughtai AI", layout="wide")

st.markdown("""
    <style>
    /* Dark Theme & Background */
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Main Chat Container Padding */
    .main .block-container { padding-bottom: 150px; } 

    /* Round Chat Bubbles */
    [data-testid="stChatMessage"] { 
        border-radius: 20px; 
        padding: 15px; 
        margin-bottom: 15px; 
        background-color: #1e1f20; 
        border: 1px solid #333; 
    }

    /* Sticky Input Box (Niche Jamha Hua) */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 30px !important;
        background-color: #0e0e0e !important;
        padding: 10px 0 !important;
        z-index: 1000;
    }

    /* Round Input Styling */
    .stChatInputContainer textarea {
        border-radius: 25px !important;
        border: 1px solid #4facfe !important;
        padding: 12px 20px !important;
    }

    /* Search Status Design */
    .search-msg {
        color: #4facfe;
        font-size: 14px;
        margin-bottom: 10px;
        font-style: italic;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SMART AUTO-SCROLL SCRIPT ---
def gemini_scroll():
    components.html(
        """
        <script>
            function scrollToBottom() {
                var docs = window.parent.document.querySelectorAll(".main");
                for (var i = 0; i < docs.length; i++) {
                    docs[i].scrollTo({ top: docs[i].scrollHeight, behavior: 'smooth' });
                }
            }
            // Execute multiple times to ensure scroll during streaming
            setTimeout(scrollToBottom, 100);
            setTimeout(scrollToBottom, 500);
            setTimeout(scrollToBottom, 1000);
        </script>
        """,
        height=0,
    )

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN INTERFACE ---
st.markdown('<h2 style="text-align:center; color:#4facfe;">✨ Chughtai AI - Vision</h2>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat", "🚜 Kisan", "🏠 Ghar"])

with tab1:
    # 1. Display All Past Messages
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Placeholder for Live Status & New Response
    status_msg = st.empty()
    
    # 2. Input Area
    if prompt := st.chat_input("Ask Gemini 3..."):
        # User message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Searching... status at the bottom
        status_msg.markdown('<p class="search-msg">🔍 Searching for info...</p>', unsafe_allow_html=True)
        gemini_scroll()

        # Web Search
        search_context = ""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                search_context = "\n".join([r['body'] for r in results])
        except: pass

        # AI Response Generation
        with st.chat_message("assistant"):
            status_msg.empty() # Remove search text when AI starts
            res_area = st.empty()
            full_text = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": f"Data: {search_context}\n\nQ: {prompt}"}]
            )
            raw_ans = completion.choices[0].message.content
            
            # Streaming Effect
            for word in raw_ans.split():
                full_text += word + " "
                res_area.markdown(full_text + "▌")
                gemini_scroll() # Auto-scroll while typing
                time.sleep(0.04)
            res_area.markdown(full_text)
            
            st.session_state.history.append({"u": prompt, "b": full_text})
            
            # Voice Output
            try:
                tts = gTTS(text=full_text, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- KISAN & GHAR TABS ---
with tab2:
    st.markdown("<div style='background:#1e1f20; padding:20px; border-radius:20px;'><h3>🚜 Kisan Calculator</h3>", unsafe_allow_html=True)
    # Baqi kisan logic yahan...
    st.markdown("</div>", unsafe_allow_html=True)
