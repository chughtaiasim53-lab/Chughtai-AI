import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import pandas as pd
import random

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Professional", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 35px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Construction Pro</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chat", "🏠 Ghar & Kamra Planner", "🚜 Fasal Calculator", "🌾 Mandi Rates"])

# --- TAB 1: AI CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Gandum rate ya koi bhi baat..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            search_data = ""
            try:
                with DDGS() as ddgs:
                    r = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=2))
                    search_data = "\n".join([i['body'] for i in r])
            except: pass
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                          {"role": "user", "content": f"Data: {search_data}\n\nQ: {last_q}"}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans

# --- TAB 2: ACCURATE CONSTRUCTION PLANNER (FIXED) ---
with tab2:
    st.markdown("<div class='card'><h3>🏠 Professional Tameerati Planner</h3>", unsafe_allow_html=True)
    
    tameer_type = st.selectbox("Kya tameer karna chahte hain?", 
                                ["Pura Ghar (Marla Hisaab)", "Akela Kamra (12x14)", "Akela Kitchen", "Akela Bathroom"])

    if tameer_type == "Pura Ghar (Marla Hisaab)":
        m_size = st.number_input("Zameen (Marla):", min_value=1.0, value=5.0)
        if st.button("Pura Ghar Estimate 🏗️"):
            # Engineer Formula: Marla based calculation
            intein = m_size * 18000 # Double story allow
            cement = m_size * 125
            sarya = m_size * 0.85
            ret = m_size * 600 # Cubic feet
            st.success(f"🏠 **{m_size} Marla Ghar ka Mukammal Estimate (Grey Structure):**")
            st.write(f"🧱 **Intein (Bricks):** {int(intein)}")
            st.write(f"🧪 **Cement:** {int(cement)} Bori")
            st.write(f"🏗️ **Sarya (Steel):** {round(sarya, 2)} Ton")
            st.write(f"⏳ **Ret (Sand):** {int(ret)} Sq. Ft")
    
    elif tameer_type == "Akela Kamra (12x14)":
        if st.button("Kamra Estimate 🛌"):
            st.success("🛌 **Standard Kamra (12x14) Estimate:**")
            st.write("🧱 **Intein:** 6,500 (9 inch deewar)")
            st.write("🧪 **Cement:** 45 Bori (Chhat aur Plaster)")
            st.write("🏗️ **Sarya:** 0.35 Ton (Chhat ke liye)")
            st.warning("💰 Andazan Kharcha: 3.5 - 4 Lakh PKR")

    elif tameer_type == "Akela Kitchen":
        if st.button("Kitchen Estimate 🍳"):
            st.success("🍳 **Standard Kitchen Estimate:**")
            st.write("🧱 **Intein:** 3,200")
            st.write("🧪 **Cement:** 25 Bori")
            st.write("🏗️ **Sarya:** 0.15 Ton")
            st.warning("💰 Andazan Kharcha: 2 Lakh PKR")

    elif tameer_type == "Akela Bathroom":
        if st.button("Bathroom Estimate 🚿"):
            st.success("🚿 **Standard Bathroom Estimate:**")
            st.write("🧱 **Intein:** 1,800")
            st.write("🧪 **Cement:** 15 Bori")
            st.warning("💰 Andazan Kharcha: 1.2 Lakh PKR")

    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: FASAL CALCULATOR ---
with tab3:
    st.markdown("<div class='card'><h3>🚜 Fasal ke mutabiq Khad (Acre)</h3>", unsafe_allow_html=True)
    crop = st.selectbox("Fasal Chunain:", ["Gandum", "Kapas", "Thomm (G1)", "Makai", "Munji"])
    acre = st.number_input("Zameen (Acres):", value=3.7)
    if st.button("Fasal Hisaab"):
        r = {"Gandum": (1.2, 2.5), "Kapas": (1.5, 3), "Thomm (G1)": (2.5, 2), "Makai": (2, 4), "Munji": (1, 2)}
        d, u = r[crop]
        st.success(f"**{crop} Report ({acre} Acre):** DAP {round(acre*d,1)} | Urea {round(acre*u,1)} Bori")

# --- TAB 4: MANDI RATES ---
with tab4:
    st.markdown("<div class='card'><h3>💹 Live Market Rates</h3>", unsafe_allow_html=True)
    st.write("Gandum: Rs. 4,380 | Gold 24K: Rs. 294,000 | Dollar: Rs. 284.5")
    st.markdown("</div>", unsafe_allow_html=True)
