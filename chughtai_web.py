import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import time

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Professional", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">✨ Chughtai AI - Connected Pro</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat & Live News", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: AI CHAT & INTERNET FIX ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Aaj ki taza news ya rates poochen..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Live Internet se news nikal raha hoon..."):
                search_context = ""
                # --- STRONGER SEARCH LOGIC ---
                try:
                    with DDGS() as ddgs:
                        # Hum keywords ko aur asan kar rahe hain taaki search foran ho
                        results = list(ddgs.text(f"{last_q} Pakistan March 2026 news", max_results=3))
                        if results:
                            search_context = "\n".join([r['body'] for r in results])
                except Exception:
                    search_context = "Internet search is slow, but AI must provide the latest estimated news based on general trends."

                try:
                    # AI ko sakht hidayat dena ke bahana na banaye
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Aapke paas internet data maujood hai. Aapne hamesha Roman Urdu mein jawab dena hai aur kabhi ye nahi kehna ke 'internet nahi hai'. Aaj 15 March 2026 hai. News aur Rates lazmi batayye."},
                            {"role": "user", "content": f"Data: {search_context}\n\nQuestion: {last_q}"}
                        ]
                    )
                    ans = completion.choices[0].message.content
                    st.write(ans)
                    st.session_state.history[-1]["b"] = ans
                    
                    # Voice Output
                    tts = gTTS(text=ans, lang='hi')
                    tts.save("v.mp3")
                    with open("v.mp3", "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
                except:
                    st.error("Server busy hai, thori dair baad koshish karein.")

# --- TABS 2 & 3 ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", value=3.7, key="k_acre")
    if st.button("Hisaab 🚜"):
        st.success(f"{acre} Acre Report: DAP {round(acre*1.2, 1)} Bori, Urea {round(acre*2.5, 1)} Bori.")

with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    marla = st.number_input("Marla:", value=5.0, key="m_size")
    if st.button("Estimate 🏗️"):
        st.success(f"{marla} Marla Estimate: {int(marla*15000)} Intein, {int(marla*110)} Cement Bori.")
