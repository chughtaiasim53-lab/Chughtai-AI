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

# --- UI STYLE (Gemini Dark Pro) ---
st.set_page_config(page_title="Chughtai AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Hide scrollbar for cleaner look but keep functionality */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }

    /* Main Container Padding */
    .main .block-container { padding-bottom: 180px; max-width: 800px; } 

    /* Gemini Style Round Bubbles */
    [data-testid="stChatMessage"] { 
        border-radius: 24px; 
        padding: 18px; 
        margin-bottom: 12px; 
        background-color: #1e1f20; 
        border: 1px solid #2d2e2f;
    }

    /* Fixed Input Box at Bottom */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 40px !important;
        background-color: #0e0e0e !important;
        z-index: 1000;
    }
    
    .stChatInputContainer textarea {
        border-radius: 28px !important;
        border: 1px solid #4facfe !important;
        padding: 14px 22px !important;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- ⚡ THE PERFECT AUTO-SCROLL SCRIPT ---
def perfect_scroll():
    components.html(
        """
        <script>
            function autoScroll() {
                const mainArea = window.parent.document.querySelector('section.main');
                if (mainArea) {
                    mainArea.scrollTo({
                        top: mainArea.scrollHeight,
                        behavior: 'smooth'
                    });
                }
            }
            // Continuous scroll during generation
            const scrollInterval = setInterval(autoScroll, 100);
            setTimeout(() => clearInterval(scrollInterval), 15000); 
        </script>
        """,
        height=0,
    )

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- INTERFACE ---
st.markdown('<h2 style="text-align:center; color:#4facfe;">✨ Chughtai AI</h2>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat", "🚜 Kisan", "🏠 Ghar"])

with tab1:
    # History Display
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    status_placeholder = st.empty()

    if prompt := st.chat_input("Yahan sawal likhein..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        status_placeholder.markdown('<p style="color:#4facfe; font-style:italic;">🔍 Searching information...</p>', unsafe_allow_html=True)
        perfect_scroll()

        # Search
        search_context = ""
        try:
            with DDGS() as ddgs:
                r = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                search_context = "\n".join([i['body'] for i in r])
        except: pass

        # AI Response
        with st.chat_message("assistant"):
            status_placeholder.empty()
            res_area = st.empty()
            full_text = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": f"Context: {search_context}\n\nQ: {prompt}"}]
            )
            raw_ans = completion.choices[0].message.content
            
            # Streaming + Auto-Scroll
            perfect_scroll() 
            for word in raw_ans.split():
                full_text += word + " "
                res_area.markdown(full_text + "▌")
                time.sleep(0.04)
            res_area.markdown(full_text)
            
            st.session_state.history.append({"u": prompt, "b": full_text})
            perfect_scroll() # Final scroll after finish

            # Voice Output
            try:
                tts = gTTS(text=full_text, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass
