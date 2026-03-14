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
    .calc-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - High Speed</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Search & Chat", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: AI CHAT & SEARCH (FIXED) ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Aaj ki news, Petrol ya Gold rate poochen..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Searching Live Data..."):
                # --- STRONGER SEARCH LOGIC ---
                search_data = ""
                try:
                    with DDGS() as ddgs:
                        # Sirf zaroori results taaki loading tez ho
                        results = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=2))
                        search_data = "\n".join([r['body'] for r in results])
                except:
                    search_data = "Search results temporarily slow, using AI internal knowledge."

                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026. Hamesha news ka jawab zaroor dein."},
                            {"role": "user", "content": f"Context: {search_data}\n\nQuestion: {last_q}"}
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
                    st.error("Groq API Busy. Thori dair baad koshish karein.")

# --- TAB 2 & 3 (Kisan aur Ghar code shamil hai) ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", value=3.7)
    if st.button("Hisaab 🚜"):
        st.success(f"{acre} Acre Report: DAP {round(acre*1.2, 1)} Bori, Urea {round(acre*2.5, 1)} Bori.")

with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Estimate 🏗️"):
        st.success(f"{marla} Marla Estimate: {int(marla*15000)} Intein, {int(marla*110)} Cement Bori.")
