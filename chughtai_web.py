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

# --- UI STYLE (Gemini Bottom Input Style) ---
st.set_page_config(page_title="Chughtai AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Messages area ko niche se khali rakha hai taaki input box ke liye jagah ho */
    .main .block-container { 
        padding-bottom: 200px !important; 
        max-width: 850px; 
        margin: auto;
    } 

    /* Round Chat Bubbles */
    [data-testid="stChatMessage"] { 
        border-radius: 25px; 
        padding: 18px; 
        margin-bottom: 12px; 
        background-color: #1e1f20; 
        border: 1px solid #2d2e2f;
    }

    /* --- CHAT BOX AT THE VERY BOTTOM --- */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 20px !important;
        left: 0;
        right: 0;
        margin-left: auto;
        margin-right: auto;
        width: 90% !important;
        max-width: 800px !important;
        background-color: transparent !important;
        z-index: 9999;
    }
    
    .stChatInputContainer textarea {
        border-radius: 35px !important;
        border: 1px solid #4facfe !important;
        background-color: #1e1f20 !important;
        padding: 15px 25px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }

    /* Hide unnecessary things */
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTO-SCROLL SCRIPT ---
def auto_scroll():
    components.html(
        """
        <script>
            function scroll() {
                var mainArea = window.parent.document.querySelector('section.main');
                if (mainArea) {
                    mainArea.scrollTo({ top: mainArea.scrollHeight, behavior: 'smooth' });
                }
            }
            setInterval(scroll, 200);
            setTimeout(() => clearInterval(), 10000);
        </script>
        """,
        height=0,
    )

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- INTERFACE ---
st.markdown('<h2 style="text-align:center; color:#4facfe; font-family: sans-serif;">✨ Chughtai AI</h2>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat", "🚜 Kisan", "🏠 Ghar"])

with tab1:
    # History
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # New Response
    if prompt := st.chat_input("Ask Chughtai AI..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        auto_scroll()

        with st.chat_message("assistant"):
            res_area = st.empty()
            full_text = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": prompt}]
            )
            ans = completion.choices[0].message.content
            
            for word in ans.split():
                full_text += word + " "
                res_area.markdown(full_text + "▌")
                time.sleep(0.04)
            res_area.markdown(full_text)
            
            st.session_state.history.append({"u": prompt, "b": full_text})
            auto_scroll()
