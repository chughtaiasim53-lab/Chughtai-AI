import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import base64

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Professional", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 35px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Bill & Builder</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chat", "💡 Bijli Bill Calc", "🏠 Ghar & Kamra Planner", "🚜 Fasal Calc"])

# --- TAB 1: AI CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])
    if prompt := st.chat_input("Gandum rate ya koi sawal..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."}); st.rerun()
    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                      {"role": "user", "content": last_q}]
        )
        st.session_state.history[-1]["b"] = completion.choices[0].message.content
        st.rerun()

# --- TAB 2: ELECTRICITY BILL CALCULATOR (NEW) ---
with tab2:
    st.markdown("<div class='card'><h3>💡 Bijli Bill Calculator (Andazan)</h3>", unsafe_allow_html=True)
    units = st.number_input("Pichle mahine ke Units likhein:", min_value=1, value=200)
    
    if st.button("Bill Calculate Karein ⚡"):
        # Pakistan Slab Rates (Approx 2026)
        if units <= 100: rate = 25
        elif units <= 200: rate = 32
        elif units <= 300: rate = 45
        elif units <= 700: rate = 55
        else: rate = 65
        
        base_bill = units * rate
        taxes = base_bill * 0.25 # 25% FPA and Taxes
        total_bill = base_bill + taxes
        
        st.success(f"⚡ **Aapka Andazan Bill: Rs. {int(total_bill)}**")
        st.info(f"Unit Rate: Rs. {rate} | Taxes: Rs. {int(taxes)}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: ACCURATE CONSTRUCTION PLANNER ---
with tab3:
    st.markdown("<div class='card'><h3>🏠 Construction Planner</h3>", unsafe_allow_html=True)
    t_type = st.selectbox("Kya tameer karna hai?", ["Pura Ghar", "Akela Kamra (12x14)", "Akela Kitchen", "Akela Bathroom"])
    
    if t_type == "Pura Ghar":
        m = st.number_input("Marla:", value=5.0)
        if st.button("Ghar Estimate"):
            st.success(f"🏠 {m} Marla: {int(m*18000)} Intein, {int(m*125)} Cement, {round(m*0.85,2)} Ton Sarya")
    elif t_type == "Akela Kamra (12x14)":
        if st.button("Kamra Estimate"):
            st.success("🛌 Kamra: 6,500 Intein, 45 Cement, 0.35 Ton Sarya")
    elif t_type == "Akela Kitchen":
        if st.button("Kitchen Estimate"):
            st.success("🍳 Kitchen: 3,200 Intein, 25 Cement, 0.15 Ton Sarya")
    elif t_type == "Akela Bathroom":
        if st.button("Bathroom Estimate"):
            st.success("🚿 Bathroom: 1,800 Intein, 15 Cement")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: FASAL CALCULATOR ---
with tab4:
    st.markdown("<div class='card'><h3>🚜 Fasal Calculator</h3>", unsafe_allow_html=True)
    crop = st.selectbox("Fasal:", ["Gandum", "Kapas", "Thomm (G1)", "Makai"])
    acre = st.number_input("Acres:", value=3.7)
    if st.button("Hisaab"):
        r = {"Gandum": (1.2, 2.5), "Kapas": (1.5, 3), "Thomm (G1)": (2.5, 2), "Makai": (2, 4)}
        d, u = r[crop]
        st.success(f"DAP: {round(acre*d,1)} | Urea: {round(acre*u,1)} Bori")
    st.markdown("</div>", unsafe_allow_html=True)
