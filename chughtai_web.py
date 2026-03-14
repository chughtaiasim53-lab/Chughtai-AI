import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Kisan Markaz", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #2ecc71; font-weight: bold; }
    .kisan-card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-top: 5px solid #2ecc71; margin-bottom: 20px; }
    .calc-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN INTERFACE ---
st.markdown('<h1 class="main-title">🌾 Chughtai AI - Professional Kisan Calculator</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Chat & Search", "🚜 All Fertilizer & Crop Calculator"])

with tab2:
    st.markdown("<div class='kisan-card'><h3>Zameen aur Fasal ki Tafseel</h3>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        acre = st.number_input("Zameen (Acres) likhein:", min_value=0.5, step=0.5, value=2.5)
    with col_b:
        fasal = st.selectbox("Fasal (Crop) select karein:", 
                            ["Rice (Basmati)", "Rice (Irri/Hybrid)", "Gandum (Wheat)", "Makka (Corn)", "Onion (Pyaz)", "Thomm (Garlic)", "Cotton"])
    
    if st.button("Mukammal Calculation Nikalein ✨"):
        # Default factors per acre
        res = {"beej": "", "dap": 0, "urea": 0, "potash": 0, "zinc": 0}
        
        if "Rice" in fasal:
            res["beej"] = "5-8 KG (Paneeri)" if "Basmati" in fasal else "8-10 KG (Hybrid)"
            res["dap"] = acre * 1
            res["urea"] = acre * 2
            res["potash"] = acre * 0.5
            res["zinc"] = acre * 5 # 5kg per acre
        elif fasal == "Thomm (Garlic)":
            res["beej"] = "200-250 KG"
            res["dap"] = acre * 2
            res["urea"] = acre * 2.5
            res["potash"] = acre * 1
            res["zinc"] = acre * 2
        elif fasal == "Onion (Pyaz)":
            res["beej"] = "3-4 KG"
            res["dap"] = acre * 1.5
            res["urea"] = acre * 2
            res["potash"] = acre * 0.5
            res["zinc"] = acre * 2
        else: # Default calculations
            res["beej"] = f"{acre * 40} KG"
            res["dap"] = acre * 1
            res["urea"] = acre * 2
            res["potash"] = acre * 0.5
            res["zinc"] = acre * 2

        st.markdown(f"### 📊 {acre} Acre {fasal} ki Fertilizer Report")
        
        st.markdown(f"<div class='calc-row'><span>🌱 **Beej (Seed):**</span> <span>{res['beej']}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **DAP Khad:**</span> <span>{res['dap']} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Urea Khad:**</span> <span>{res['urea']} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Potash (SOP):**</span> <span>{res['potash']} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Zinc (33%):**</span> <span>{res['zinc']} KG</span></div>", unsafe_allow_html=True)
        
        st.info("💡 **Note:** Ye calculation aik average zameen ke liye hai. Behtar paidawar ke liye zameen ka test zaroor karwayein.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    # Chat Logic (as before)
    for chat in st.session_state.chat_history:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.write(chat["bot"])

    if prompt := st.chat_input("Farming, Gold ya Petrol rates poochen..."):
        st.session_state.chat_history.append({"user": prompt, "bot": "Thinking..."})
        st.rerun()

# Processing Logic (same)
if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Thinking...":
    last_prompt = st.session_state.chat_history[-1]["user"]
    with st.chat_message("assistant"):
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{last_prompt} Pakistan 2026", max_results=2)]
            context = "\n".join([r['body'] for r in results])
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                      {"role": "user", "content": last_prompt}]
        )
        ans = completion.choices[0].message.content
        st.write(ans)
        st.session_state.chat_history[-1]["bot"] = ans
        
        tts = gTTS(text=ans, lang='hi')
        tts.save("v.mp3")
        with open("v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
