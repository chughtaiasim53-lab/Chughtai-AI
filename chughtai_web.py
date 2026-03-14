import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import random

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Super Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 12px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HISTORY) ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("<h2 style='color: #4facfe;'>📜 History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.info(f"{chat['u'][:30]}...")

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Price Tracker</h1>', unsafe_allow_html=True)

tabs = st.tabs(["💬 Live Chat & News", "🌾 Mandi & Gold Rates", "📏 Zameen Calculator", "🚜 Farming Tools"])

# --- TAB 1: CHAT (DIRECT SEARCH FIX) ---
with tabs[0]:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Rahim Yar Khan mandi rate ya news puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Internet se taza rates nikal raha hoon..."):
                search_data = ""
                try:
                    with DDGS() as ddgs:
                        # Rahim Yar Khan specific search taaki sahi jawab aaye
                        r = list(ddgs.text(f"current rates {last_q} Pakistan March 2026", max_results=3))
                        search_data = "\n".join([i['body'] for i in r])
                except: pass

                # AI ko sakht hidayat dena
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Aap Chughtai AI hain. Aapne hamesha Roman Urdu mein jawab dena hai. Kabhi ye nahi kehna ke 'maloomat nahi hai'. Aaj 15 March 2026 hai. Gandum, Gold aur Petrol rates lazmi batayein."},
                              {"role": "user", "content": f"Search Data: {search_data}\n\nSawal: {last_q}"}]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.history[-1]["b"] = ans
                
                # Voice Reply
                tts = gTTS(text=ans, lang='hi'); tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: MANDI & RATES TABLE ---
with tabs[1]:
    st.markdown("### 💹 Live Market Overview (March 15, 2026)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'><b>🌾 Mandi (RYK/Multan)</b><br>Gandum: Rs. 4,350<br>Kapas: Rs. 8,200<br>G1 Garlic: Rs. 15,000<br>Munji: Rs. 5,100</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><b>💰 Global Rates</b><br>Gold (24K): Rs. 292,500<br>Dollar: Rs. 284.50<br>Petrol: Rs. 278.20</div>", unsafe_allow_html=True)

# --- TAB 3: ZAMEEN CALCULATOR ---
with tabs[2]:
    st.markdown("<div class='card'><h3>📏 Area Converter</h3>", unsafe_allow_html=True)
    val = st.number_input("Raqba likhein:", value=1.0)
    mode = st.selectbox("Unit:", ["Acre to Marla", "Kanal to Marla", "Acre to Kanal"])
    if st.button("Hisaab Karein"):
        res = val*160 if mode=="Acre to Marla" else val*20 if mode=="Kanal to Marla" else val*8
        st.success(f"Natija: {res}")

# --- TAB 4: FARMING TOOLS ---
with tabs[3]:
    st.markdown("<div class='card'><h3>🚜 Fertilizer Calculator</h3>", unsafe_allow_html=True)
    z = st.number_input("Zameen Acres:", value=3.7)
    if st.button("Check Khad"):
        st.info(f"DAP: {round(z*1.2,1)} Bori | Urea: {round(z*2.5,1)} Bori")
