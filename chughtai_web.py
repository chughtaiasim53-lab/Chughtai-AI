import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import speech_recognition as sr # Naya Voice-to-Text function

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Voice Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HISTORY) ---
if "history" not in st.session_state:
    st.session_state.history = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Voice & History</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("### 📜 Purani Baatein")
    if st.button("🗑️ Sab Mita Dein"):
        st.session_state.history = []
        st.rerun()
    st.divider()
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:35]}...")

tab1, tab2, tab3 = st.tabs(["💬 Chat & Voice", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: VOICE TO TEXT & CHAT ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("🎤 **Bol kar sawal puchiye:**")
    
    if st.button("Record Voice (Bolna shuru karein)"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("AI sun raha hai... Bolen!")
            audio = r.listen(source)
            try:
                st.session_state.voice_text = r.recognize_google(audio, language='ur-PK')
                st.success(f"Aapne kaha: {st.session_state.voice_text}")
            except:
                st.error("Awaz samajh nahi aayi, dobara koshish karein.")
    
    # Chat Display
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Input Box (Voice text auto-fill)
    prompt = st.chat_input("Yahan likhein ya oper se Record karein...", key="chat_input")
    
    # Agar voice se text aaya hai ya likha hai
    final_input = st.session_state.voice_text if st.session_state.voice_text and not prompt else prompt

    if final_input:
        st.session_state.history.append({"u": final_input, "b": "Thinking..."})
        st.session_state.voice_text = "" # Clear voice cache
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            search_context = ""
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(f"{last_q} Pakistan news 2026", max_results=2))
                    search_context = "\n".join([r['body'] for r in results])
            except: pass

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                          {"role": "user", "content": f"Context: {search_context}\n\nQuestion: {last_q}"}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            
            # Voice Reply (AI bolega bhi)
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2 & 3 (Kisan & Ghar) ---
with tab2:
    st.write("### 🚜 Kisan Calculator")
    acre = st.number_input("Acres:", value=3.7)
    if st.button("Hisaab"): st.success(f"DAP: {round(acre*1.2,1)} | Urea: {round(acre*2.5,1)}")

with tab3:
    st.write("### 🏠 Ghar Planner")
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Estimate"): st.success(f"Intein: {int(marla*15000)} | Cement: {int(marla*110)}")
