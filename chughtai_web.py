import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import random
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Super Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 12px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e1f20; border-radius: 5px; padding: 10px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #4facfe;'>📜 History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.info(f"{chat['u'][:30]}...")

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Super App</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & News", "🌾 Mandi & Gold", "📏 Zameen Calc", "🚜 Kisan & Weather"])

# --- TAB 1: SMART CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Gandum rate, Petrol, ya Gold rate puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Internet se data nikal raha hoon..."):
                search_data = ""
                try:
                    with DDGS() as ddgs:
                        r = list(ddgs.text(f"current price {last_q} Pakistan March 2026", max_results=3))
                        search_data = "\n".join([i['body'] for i in r])
                except: pass

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Aap Chughtai AI hain. Aapne Roman Urdu mein jawab dena hai. Kabhi ye nahi kehna ke maloomat nahi hai. Aaj 15 March 2026 hai. Rates lazmi batayein."},
                              {"role": "user", "content": f"Search Data: {search_data}\n\nSawal: {last_q}"}]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.history[-1]["b"] = ans
                tts = gTTS(text=ans, lang='hi'); tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: LIVE RATES ---
with tab2:
    st.markdown("### 💹 Market Watch (15 March 2026)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'><b>🌾 Mandi Rates (Punjab)</b><br>Gandum: Rs. 4,300 - 4,450<br>Kapas: Rs. 8,100<br>Thum (G1): Rs. 14,500</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><b>💰 Currency & Gold</b><br>Gold (24K): Rs. 294,000<br>Dollar: Rs. 284.10<br>Riyal: Rs. 75.80</div>", unsafe_allow_html=True)

# --- TAB 3: ZAMEEN CONVERTER ---
with tab3:
    st.markdown("<div class='card'><h3>📏 Area Converter</h3>", unsafe_allow_html=True)
    val = st.number_input("Raqba (Value):", value=1.0)
    mode = st.selectbox("Unit chunain:", ["Acre to Marla", "Kanal to Marla", "Acre to Kanal", "Marla to Sq. Feet"])
    if st.button("Convert"):
        if mode=="Acre to Marla": res = val*160
        elif mode=="Kanal to Marla": res = val*20
        elif mode=="Acre to Kanal": res = val*8
        else: res = val*272.25
        st.success(f"Natija: {res}")

# --- TAB 4: KISAN & WEATHER ---
with tab4:
    st.markdown("<div class='card'><h3>☁️ Weather & Farming</h3>", unsafe_allow_html=True)
    st.info("🌦️ **Weather Alert:** Agle 24 ghanton mein Rahim Yar Khan mein halki baarish ka imkan hai. Gandum ki fasal ka khayal rakhein.")
    z = st.number_input("Zameen (Acres):", value=3.7)
    if st.button("Fertilizer Plan"):
        st.write(f"🧪 **DAP:** {round(z*1.2, 1)} Bori")
        st.write(f"🧪 **Urea:** {round(z*2.5, 1)} Bori")
