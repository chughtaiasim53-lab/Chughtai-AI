import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- GEMINI PRO UI CUSTOMIZATION ---
st.set_page_config(page_title="Gemini 3 Pro", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    /* Dark Background like Gemini */
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Center Title Style */
    .gemini-title {
        font-family: 'Google Sans', Arial;
        font-size: 40px;
        font-weight: 500;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 50px;
    }
    
    /* Central Search Bar Style */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #3c4043 !important;
        background-color: #1e1f20 !important;
        margin-bottom: 20px;
    }

    /* Suggestion Buttons Style */
    .stButton>button {
        border-radius: 20px;
        background-color: #1e1f20;
        color: #e3e3e3;
        border: 1px solid #444746;
        padding: 10px 20px;
        font-size: 14px;
    }
    .stButton>button:hover {
        background-color: #333537;
        border-color: #8e918f;
    }

    /* Hide Streamlit elements for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for History (Optional but useful)
with st.sidebar:
    st.markdown("### 📜 Recent")
    if "history" not in st.session_state:
        st.session_state.history = []
    for h in st.session_state.history[-5:]:
        st.write(f"📁 {h[:20]}...")

# --- Main Interface ---
st.markdown('<h1 class="gemini-title">✨ Hi Qadir Dad<br><span style="color:#e3e3e3">Where should we start?</span></h1>', unsafe_allow_html=True)

# Central Buttons (Like Screenshot)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🖼️ Create image"):
        st.session_state.mode = "image"
with col2:
    if st.button("🎵 Create music"):
        st.info("Music tool coming soon!")
with col3:
    if st.button("💡 Help me learn"):
        st.session_state.mode = "chat"
with col4:
    if st.button("📝 Write anything"):
        st.session_state.mode = "chat"

# --- Chat/Search Logic ---
if prompt := st.chat_input("Ask Gemini 3"):
    st.session_state.history.append(prompt)
    
    # Check if user wants image or chat
    if "create image" in prompt.lower() or (getattr(st.session_state, 'mode', '') == "image"):
        with st.spinner("🎨 Generating image..."):
            img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1080&height=1080&model=flux"
            st.image(img_url, caption=f"Generated: {prompt}")
            st.session_state.mode = "chat" # Reset to chat
    else:
        # Standard Search & Chat
        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching live data..."):
                    with DDGS() as ddgs:
                        r = [res for res in ddgs.text(f"{prompt} Pakistan latest 2026", max_results=3)]
                        context = "\n".join([res['body'] for res in r])
                
                aaj = datetime.date.today().strftime("%d %B %Y")
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"Aap Gemini 3 Pro hain. Roman Urdu mein jawab dein. Aaj {aaj} hai. Data: {context}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                ans = completion.choices[0].message.content
                st.markdown(ans)
                
                # Voice Output
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
