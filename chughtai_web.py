import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI Super App", layout="wide")

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
    st.markdown("<h2 style='color: #4facfe;'>📜 Chat History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All"):
        st.session_state.history = []
        st.rerun()
    st.write("---")
    for i, chat in enumerate(reversed(st.session_state.history)):
        st.info(f"{chat['u'][:30]}...")

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI Super App</h1>', unsafe_allow_html=True)

tabs = st.tabs(["💬 Chat & News", "🌾 Mandi & Rates", "📏 Zameen Calculator", "🚜 Kisan & Ghar"])

# --- TAB 1: CHAT ---
with tabs[0]:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Kuch bhi puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                search_data = ""
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f"{last_q} Pakistan news 2026", max_results=2))
                        search_data = "\n".join([r['body'] for r in results])
                except: pass

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                              {"role": "user", "content": f"Data: {search_data}\n\nQ: {last_q}"}]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.history[-1]["b"] = ans
                tts = gTTS(text=ans, lang='hi'); tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: LIVE RATES (Mandi, Gold, Currency) ---
with tabs[1]:
    st.markdown("### 💹 Live Market Rates (Estimated)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'><b>🌾 Mandi Rates (Per 40kg)</b><br>Gandum: Rs. 4,200<br>Kapas: Rs. 8,500<br>Thum (Garlic): Rs. 12,000</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><b>💰 Currency & Gold</b><br>Dollar: Rs. 285<br>Sona (24K): Rs. 215,000<br>Riyal: Rs. 76</div>", unsafe_allow_html=True)

# --- TAB 3: ZAMEEN CALCULATOR ---
with tabs[2]:
    st.markdown("<div class='card'><h3>📏 Zameen Paimaish Converter</h3>", unsafe_allow_html=True)
    val = st.number_input("Value likhein:", min_value=0.0, value=1.0)
    unit = st.selectbox("Convert karein:", ["Acre to Marla", "Kanal to Marla", "Acre to Kanal"])
    if st.button("Convert"):
        if unit == "Acre to Marla": res = val * 160
        elif unit == "Kanal to Marla": res = val * 20
        else: res = val * 8
        st.success(f"Result: {res} units")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: KISAN & GHAR ---
with tabs[3]:
    st.write("### 🚜 Farming & Construction Tools")
    a = st.number_input("Zameen Acres:", value=3.7)
    if st.button("Khad ka Hisaab"):
        st.info(f"DAP: {round(a*1.2,1)} Bori | Urea: {round(a*2.5,1)} Bori")
    
    st.write("---")
    m = st.number_input("Ghar Marla:", value=5.0)
    if st.button("Material Estimate"):
        st.info(f"Intein: {int(m*15000)} | Cement: {int(m*110)} Bori")
