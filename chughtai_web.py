import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Super App", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    .calc-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - All In One</h1>', unsafe_allow_html=True)

# --- TABS FOR DIFFERENT FEATURES ---
tab1, tab2, tab3 = st.tabs(["💬 Search & AI Chat", "🚜 Kisan Markaz", "🏠 Ghar & Zameen Planner"])

# --- TAB 1: AI CHAT & SEARCH ---
with tab1:
    # History Sidebar
    with st.sidebar:
        st.title("📜 Chat History")
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
        for chat in reversed(st.session_state.history):
            st.write(f"👉 {chat['u'][:30]}...")

    # Display Chat
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye (e.g. Aaj ka Sona ya Petrol rate?)..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Searching Live Data..."):
                try:
                    search_data = ""
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=3))
                        search_data = "\n".join([r['body'] for r in results])
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
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
                    st.error("Search Fail. Dobara koshish karein.")

# --- TAB 2: KISAN CALCULATOR ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Professional Kisan Calculator</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        acre = st.number_input("Zameen (Acres):", min_value=0.1, step=0.1, value=3.7, key="kisan_acre")
    with col2:
        fasal = st.selectbox("Fasal Chunain:", ["Gandum (Wheat)", "Rice (Basmati)", "Rice (Hybrid)", "Makka (Corn)", "Thomm (Garlic/G1)", "Onion (Pyaz)"])
    
    if st.button("Hisaab Lagayein 🚜"):
        # Accurate formulas per acre
        rates = {
            "Gandum (Wheat)": {"b": 50, "d": 1, "u": 2, "p": 0.5, "z": 2},
            "Rice (Basmati)": {"b": 7, "d": 1, "u": 2, "p": 0.5, "z": 5},
            "Rice (Hybrid)": {"b": 9, "d": 1.5, "u": 3, "p": 0.75, "z": 5},
            "Makka (Corn)": {"b": 10, "d": 1.5, "u": 3.5, "p": 1, "z": 3},
            "Thomm (Garlic/G1)": {"b": 250, "d": 2, "u": 2.5, "p": 1, "z": 3},
            "Onion (Pyaz)": {"b": 4, "d": 1.5, "u": 2, "p": 0.5, "z": 2}
        }
        f = rates[fasal]
        st.success(f"### {acre} Acre {fasal} Report:")
        st.markdown(f"<div class='calc-row'><span>🌱 Beej (Seed):</span> <span>{round(acre * f['b'], 2)} KG</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 DAP Khad:</span> <span>{round(acre * f['d'], 2)} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 Urea Khad:</span> <span>{round(acre * f['u'], 2)} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 Potash:</span> <span>{round(acre * f['p'], 2)} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 Zinc (33%):</span> <span>{round(acre * f['z'], 2)} KG</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: CONSTRUCTION & ZAMEEN PLANNER ---
with tab3:
    st.markdown("<div class='card'><h3>🏠 Tameerati Planner (Ghar & Zameen)</h3>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        marla = st.number_input("Zameen (Marla):", min_value=1.0, step=1.0, value=5.0)
    with col4:
        typ = st.selectbox("Kya banana hai?", ["Ghar (Residential)", "Dukanain (Commercial)"])

    if st.button("Plan Banayein 🏗️"):
        if typ == "Ghar (Residential)":
            plan = "3 Bedrooms, 3 Bath" if marla <= 5 else "5 Bedrooms, 5 Bath, Lawn"
            intein = marla * 15000
            cement = marla * 110
            sarya = marla * 0.9
            st.success(f"🏠 {marla} Marla Ghar ka Andaza:")
            st.write(f"**Naqsha:** {plan}")
        else:
            dukan = int(marla * 2)
            intein = marla * 12000
            cement = marla * 90
            sarya = marla * 0.7
            st.success(f"🏢 {marla} Marla Commercial Plan:")
            st.write(f"Is jagah par **{dukan} Dukanain** ban sakti hain.")

        st.markdown(f"<div class='calc-row'><span>🧱 Intein (Bricks):</span> <span>{int(intein)} pieces</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 Cement:</span> <span>{int(cement)} Boriyan</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🏗️ Sarya (Steel):</span> <span>{round(sarya, 2)} Ton</span></div>", unsafe_allow_html=True)
        st.info("💰 Note: Grey structure ka kharcha takreeban 12-15 lakh per marla aayega (March 2026 rates).")
    st.markdown("</div>", unsafe_allow_html=True)
