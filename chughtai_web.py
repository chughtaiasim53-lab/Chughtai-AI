import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64

# --- API Connection ---
# Aapka Groq API Key
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

st.markdown('<h1 class="main-title">✨ Chughtai AI - Connected</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat & Live News", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: AI CHAT & INTERNET SEARCH ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Aaj ki news ya rates poochen..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Internet se maloomat le raha hoon..."):
                search_context = ""
                # --- INTERNET ACCESS LOGIC ---
                try:
                    with DDGS() as ddgs:
                        # Hum internet se taza tareen news utha rahe hain
                        results = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=3))
                        if results:
                            search_context = "\n".join([r['body'] for r in results])
                except Exception as e:
                    search_context = "Internet search slow hai, AI purani maloomat use karega."

                try:
                    # Groq AI ko context dena
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Aapke paas internet access hai. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                            {"role": "user", "content": f"Internet Data: {search_context}\n\nSawal: {last_q}"}
                        ]
                    )
                    ans = completion.choices[0].message.content
                    st.write(ans)
                    st.session_state.history[-1]["b"] = ans
                    
                    # Voice
                    tts = gTTS(text=ans, lang='hi')
                    tts.save("v.mp3")
                    with open("v.mp3", "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
                except:
                    st.error("API Limit poori ho gayi hai. Thori dair baad koshish karein.")

# --- TABS 2 & 3 (Kisan aur Ghar Planner) ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", value=3.7, key="acre_input")
    if st.button("Hisaab 🚜"):
        st.success(f"{acre} Acre Report: DAP {round(acre*1.2, 1)} Bori, Urea {round(acre*2.5, 1)} Bori.")

with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    marla = st.number_input("Marla:", value=5.0, key="marla_input")
    if st.button("Estimate 🏗️"):
        st.success(f"{marla} Marla Estimate: {int(marla*15000)} Intein, {int(marla*110)} Cement Bori.")
