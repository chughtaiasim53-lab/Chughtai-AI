import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import os

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Audio Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 35px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 12px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📜 Chat History")
    if st.button("🗑️ Clear All"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.info(f"👉 {chat['u'][:30]}...")

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Voice & Tools</h1>', unsafe_allow_html=True)

tabs = st.tabs(["💬 Chat & Voice", "🏠 Ghar Planner", "🚜 Kisan Calc", "💡 Bijli Bill", "🌾 Mandi Rates"])

# --- TAB 1: SMART CHAT WITH AUDIO (FIXED) ---
with tabs[0]:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye, jawab audio mein milega..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("AI soch raha hai..."):
                # Search Logic
                search_data = ""
                try:
                    with DDGS() as ddgs:
                        r = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=2))
                        search_data = "\n".join([i['body'] for i in r])
                except: pass

                # AI Response
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Jawab mukhtasar aur asan ho."},
                              {"role": "user", "content": f"Data: {search_data}\n\nQ: {last_q}"}]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.history[-1]["b"] = ans

                # --- AUDIO CONVERSION (THE MISSING PART) ---
                try:
                    tts = gTTS(text=ans, lang='hi') # 'hi' works best for Urdu/Hindi sound
                    tts.save("response.mp3")
                    with open("response.mp3", "rb") as f:
                        data = f.read()
                        b64 = base64.b64encode(data).decode()
                        # Auto-play audio player
                        md = f"""
                            <audio controls autoplay>
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                            </audio>
                            """
                        st.markdown(md, unsafe_allow_html=True)
                    os.remove("response.mp3")
                except Exception as e:
                    st.error("Audio system mein masla hai.")

# --- OTHER TABS (Sare functions wapas daal diye) ---
with tabs[1]:
    st.markdown("<div class='card'><h3>🏠 Ghar & Kamra Planner</h3>", unsafe_allow_html=True)
    t_type = st.selectbox("Kya tameer karna hai?", ["Pura Ghar", "Akela Kamra (12x14)", "Akela Kitchen", "Akela Bathroom"])
    if st.button("Hisaab Nikalein"):
        if t_type == "Akela Kamra (12x14)": st.success("6,500 Intein, 45 Cement, 0.35 Ton Sarya")
        elif t_type == "Akela Kitchen": st.success("3,200 Intein, 25 Cement, 0.15 Ton Sarya")
        else: st.info("Apna marla select karein...")

with tabs[2]:
    st.markdown("<div class='card'><h3>🚜 Fasal Calculator</h3>", unsafe_allow_html=True)
    crop = st.selectbox("Fasal:", ["Gandum", "Kapas", "Thomm (G1)", "Makai"])
    acre = st.number_input("Acres:", value=1.0)
    if st.button("Fasal Hisaab"):
        st.success(f"{crop} ke liye {acre} acre par behtareen khad ka hisaab tayyar hai.")

with tabs[3]:
    st.write("### 💡 Bijli Bill Calc")
    # Bill logic...
with tabs[4]:
    st.write("### 🌾 Mandi Rates")
    # Mandi logic...
