import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- GEMINI PRO DARK UI ---
st.set_page_config(page_title="Gemini 3 Pro", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .gemini-title {
        font-family: 'Google Sans', Arial;
        font-size: 45px;
        font-weight: 500;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 30px;
    }
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #3c4043 !important;
        background-color: #1e1f20 !important;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #1e1f20;
        color: #e3e3e3;
        border: 1px solid #444746;
        width: 100%;
    }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN / NAME LOGIC ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Agar naam nahi pata, to pehle poocho
if st.session_state.user_name is None:
    st.markdown('<h1 class="gemini-title">Welcome to Gemini 3</h1>', unsafe_allow_html=True)
    with st.container():
        st.write("### Hello! Aapka naam kya hai?")
        naam = st.text_input("Apna naam yahan likhein...", placeholder="e.g. Asim Chughtai")
        if st.button("Aagay Barhein ✨"):
            if naam:
                st.session_state.user_name = naam
                st.rerun()
            else:
                st.warning("Plz apna naam likhein!")
    st.stop() # Jab tak naam nahi milega, niche wala code nahi chalega

# --- MAIN GEMINI INTERFACE (Jab naam mil jaye) ---
user_name = st.session_state.user_name
st.markdown(f'<h1 class="gemini-title">✨ Hi {user_name}<br><span style="color:#e3e3e3">Where should we start?</span></h1>', unsafe_allow_html=True)

# Central Suggestion Buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🖼️ Create image"): st.toast("Image mode active! Just type what you want.")
with col2:
    if st.button("🎵 Create music"): st.info("Music feature coming soon!")
with col3:
    if st.button("💡 Help me learn"): pass
with col4:
    if st.button("📝 Write anything"): pass

# --- Search & Chat Logic ---
if prompt := st.chat_input(f"Ask Gemini 3, {user_name}..."):
    
    # Image logic (if keyword found)
    if "create image" in prompt.lower() or "tasveer" in prompt.lower():
        with st.spinner("🎨 Generating image..."):
            img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1080&height=1080&model=flux"
            st.image(img_url, caption=f"Result for: {prompt}")
    else:
        # Accurate Search Chat
        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching live data..."):
                    with DDGS() as ddgs:
                        r = [res for res in ddgs.text(f"{prompt} Pakistan 2026", max_results=3)]
                        context = "\n".join([res['body'] for res in r])
                
                aaj = datetime.date.today().strftime("%d %B %Y")
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"Aap Gemini 3 Pro hain. User ka naam {user_name} hai. Roman Urdu mein jawab dein. Date: {aaj}. Context: {context}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                ans = completion.choices[0].message.content
                st.markdown(ans)
                
                # Voice
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
