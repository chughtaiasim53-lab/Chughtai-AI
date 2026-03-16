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

# --- UI STYLE (Gemini Style + Auto Scroll Fix) ---
st.set_page_config(page_title="Chughtai AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Round Containers */
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 25px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 25px; border: 1px solid #333; margin-bottom: 20px; }
    
    /* Round Chat Bubbles */
    [data-testid="stChatMessage"] { border-radius: 25px; padding: 15px; margin-bottom: 15px; border: 1px solid #262730; background-color: #1e1f20; }
    
    /* Round Input Box */
    .stChatInputContainer textarea { border-radius: 30px !important; border: 1px solid #4facfe !important; padding: 12px 25px !important; background-color: #0e0e0e !important; }
    
    /* Hide top padding for cleaner look */
    .block-container { padding-top: 2rem; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTO SCROLL JAVASCRIPT ---
def auto_scroll():
    components.html(
        """
        <script>
            var itv = setInterval(function() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: ''}, '*');
                var chatContainer = window.parent.document.querySelector('.main');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }, 100);
            setTimeout(function() { clearInterval(itv); }, 5000); 
        </script>
        """,
        height=0,
    )

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Smart Chat", "🌾 Agri Plan", "🏠 Build Plan"])

# --- TAB 1: SMART CHAT ---
with tab1:
    # Display History
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Input Section
    if prompt := st.chat_input("Sawal puchiye..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        # Assistant Response Container
        with st.chat_message("assistant"):
            status_placeholder = st.empty() # Search status yahan niche ayega
            response_placeholder = st.empty()
            full_response = ""
            
            # 1. Searching (End par show hoga)
            status_placeholder.markdown("🔍 *Maloomaat talash ki ja rahi hain...*")
            search_context = ""
            try:
                with DDGS() as ddgs:
                    r = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                    search_context = "\n".join([i['body'] for i in r])
            except: pass
            
            # 2. AI Processing
            status_placeholder.empty() # Search khatam, ab response shuru
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 16 March 2026."},
                          {"role": "user", "content": f"Context: {search_context}\n\nQuestion: {prompt}"}]
            )
            ans = completion.choices[0].message.content
            
            # 3. Streaming + Auto Scroll
            auto_scroll() # Start auto scroll
            for chunk in ans.split():
                full_response += chunk + " "
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.06)
            response_placeholder.markdown(full_response)
            
            # Save to history
            st.session_state.history.append({"u": prompt, "b": full_response})
            
            # 4. Voice Output
            try:
                tts = gTTS(text=full_response, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- TAB 2 & 3 (Same logic as before) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Per Acre Agri Management</h3>", unsafe_allow_html=True)
    # (Agri Calculator Logic...)
