import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import pandas as pd

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - All In One", layout="wide")

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
if "kharcha_list" not in st.session_state: st.session_state.kharcha_list = []

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("<h2 style='color: #4facfe;'>📜 History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.info(f"👉 {chat['u'][:30]}...")

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Super App</h1>', unsafe_allow_html=True)

# Ab saare 5 Tabs ek saath hain
tabs = st.tabs(["💬 Chat & News", "🚜 Kisan & Ghar", "📝 Kharcha Register", "🌊 Tube-well Calc", "🌾 Mandi Rates"])

# --- TAB 1: SMART CHAT ---
with tabs[0]:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Gandum rate ya koi bhi sawal..."):
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
            tts = gTTS(text=ans, lang='hi'); tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: KISAN & GHAR (PURANE FUNCTIONS WAPAS) ---
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
        acre = st.number_input("Zameen (Acres):", value=3.7, key="k_acre")
        if st.button("Hisaab Lagayein"):
            st.success(f"DAP: {round(acre*1.2, 1)} Bori | Urea: {round(acre*2.5, 1)} Bori")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
        marla = st.number_input("Marla Size:", value=5.0, key="m_size")
        if st.button("Estimate Check"):
            st.success(f"Intein: {int(marla*15000)} | Cement: {int(marla*110)} Bori")
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: KHARCHA REGISTER ---
with tabs[2]:
    st.markdown("<div class='card'><h3>📝 Digital Kharcha Register</h3>", unsafe_allow_html=True)
    item = st.text_input("Kharcha kis cheez par hua?")
    amount = st.number_input("Rupay (Amount):", min_value=0)
    if st.button("Save Kharcha"):
        st.session_state.kharcha_list.append({"Item": item, "Amount": amount})
        st.success("Save ho gaya!")
    if st.session_state.kharcha_list:
        df = pd.DataFrame(st.session_state.kharcha_list)
        st.table(df)
        st.write(f"**Total: Rs. {df['Amount'].sum()}**")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: TUBE-WELL CALC ---
with tabs[3]:
    st.markdown("<div class='card'><h3>🌊 Tube-well Diesel Calc</h3>", unsafe_allow_html=True)
    h = st.number_input("Kitne ghante chala?", value=1.0)
    dr = st.number_input("Diesel Price:", value=280.0)
    if st.button("Kharcha Calculate"):
        total = h * 3.5 * dr # 3.5 litre average per hour
        st.error(f"Total Diesel Kharcha: Rs. {int(total)}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 5: MANDI RATES ---
with tabs[4]:
    st.markdown("<div class='card'><h3>💹 Live Market Rates</h3>", unsafe_allow_html=True)
    st.write("Gandum: Rs. 4,380 | Gold 24K: Rs. 294,000 | Dollar: Rs. 284.5")
    st.markdown("</div>", unsafe_allow_html=True)
