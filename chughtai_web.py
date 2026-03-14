import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Markaz", layout="wide", page_icon="✨")

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
st.markdown('<h1 class="main-title">✨ Chughtai AI - Professional</h1>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["💬 Search & Chat", "🚜 Kisan Markaz", "🏠 Ghar & Kamra Planner"])

# --- TAB 1: AI CHAT & SEARCH ---
with tab1:
    with st.sidebar:
        st.title("📜 Purani Baatein")
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
        for chat in reversed(st.session_state.history):
            st.write(f"👉 {chat['u'][:30]}...")

    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye (Petrol rate, Gold, ya koi bhi baat)..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Checking official data..."):
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
                    
                    # Voice Output
                    tts = gTTS(text=ans, lang='hi')
                    tts.save("v.mp3")
                    with open("v.mp3", "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
                except:
                    st.error("Connection slow hai. Dobara koshish karein.")

# --- TAB 2: ACCURATE KISAN CALCULATOR ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Professional Kisan Calculator</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        acre = st.number_input("Zameen (Acres):", min_value=0.1, step=0.1, value=3.7)
    with col2:
        fasal = st.selectbox("Fasal Chunain:", ["Gandum (Wheat)", "Rice (Basmati)", "Rice (Hybrid)", "Makka (Corn)", "Thomm (Garlic/G1)", "Onion (Pyaz)"])
    
    if st.button("Hisaab Lagayein 🚜"):
        # Fixed formulas per acre
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

# --- TAB 3: CONSTRUCTION PLANNER ---
with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar, Kamra & Kitchen Planner</h3>", unsafe_allow_html=True)
    tameer_type = st.selectbox("Kya tameer karna chahte hain?", 
                                ["Pura Ghar (Marla Hisaab)", "Sirf Ek Kamra (12x14)", "Sirf Kitchen", "Sirf Bathroom"])

    if tameer_type == "Pura Ghar (Marla Hisaab)":
        m_size = st.number_input("Zameen (Marla):", min_value=1.0, value=5.0)
        if st.button("Ghar ka Estimate Nikalein"):
            intein = m_size * 15000; cement = m_size * 110; sarya = m_size * 0.9
            st.success(f"🏠 {m_size} Marla ka Estimate:")
            st.markdown(f"<div class='calc-row'><span>🧱 Intein (Bricks):</span> <span>{int(intein)}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='calc-row'><span>🧪 Cement:</span> <span>{int(cement)} Bori</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='calc-row'><span>🏗️ Sarya (Steel):</span> <span>{round(sarya, 2)} Ton</span></div>", unsafe_allow_html=True)
    else:
        if st.button(f"{tameer_type} ka Estimate Nikalein"):
            if tameer_type == "Sirf Ek Kamra (12x14)": i, c, s, k = 4500, 35, 0.25, "2.5 - 3 Lakh"
            elif tameer_type == "Sirf Kitchen": i, c, s, k = 2200, 22, 0.15, "1.5 - 2 Lakh"
            elif tameer_type == "Sirf Bathroom": i, c, s, k = 1200, 15, 0.10, "1 - 1.3 Lakh"
            
            st.success(f"🛠️ {tameer_type} Report:")
            st.markdown(f"<div class='calc-row'><span>🧱 Intein:</span> <span>{i}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='calc-row'><span>🧪 Cement:</span> <span>{c} Bori</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='calc-row'><span>🏗️ Sarya:</span> <span>{s} Ton</span></div>", unsafe_allow_html=True)
            st.warning(f"💰 Andazan Kharcha (Grey Structure): {k} PKR")
    st.markdown("</div>", unsafe_allow_html=True)
