import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Kisan Expert", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">🚜 Chughtai AI - Kisan Markaz</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 AI Chat & Voice", "🌾 Fertilizer & Spray Plan", "🏠 Ghar Planner"])

# --- TAB 1: CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Fasal ya bemari ke bare mein puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        with st.chat_message("assistant"):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                          {"role": "user", "content": prompt}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            
            # Voice Output
            try:
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- TAB 2: KISAN CALCULATOR (KHAD & SPRAY) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Per Acre Full Management Plan</h3>", unsafe_allow_html=True)
    
    crop = st.selectbox("Fasal Chunain:", 
                        ["Lehsan (Garlic)", "Gandum (Wheat)", "Kapas (Cotton)", "Dhan (Rice)", "Makai (Maize)"])
    
    acre = st.number_input("Zameen (Acres):", value=2.5, min_value=0.1, step=0.1)
    
    if st.button("Mukammal Plan Dekhein"):
        st.markdown(f"### 📋 {crop} Management for {acre} Acre")
        
        # Details according to your crop selection
        if crop == "Lehsan (Garlic)":
            st.success("**Fertilizer (Khad):** 2.5 Bori DAP, 2 Bori Urea, 2 Bori Potash (Per Acre)")
            st.info("**Spray:** Fungicide (Agi-M), Weedicide (Pendimethalin), Amino Acid (For Growth)")
            st.warning(f"**Seed Total:** {200*acre} - {250*acre} KG")

        elif crop == "Gandum (Wheat)":
            st.success("**Fertilizer (Khad):** 1.25 Bori DAP, 2 Bori Urea (Per Acre)")
            st.info("**Spray:** Weedicide (Chora/Nokila Patta), Fungicide (Agar Zarorat ho)")
            st.warning(f"**Seed Total:** {40*acre} - {50*acre} KG")

        elif crop == "Kapas (Cotton)":
            st.success("**Fertilizer (Khad):** 1.5 Bori DAP, 3 Bori Urea, 1 Bori Potash (Per Acre)")
            st.info("**Spray:** Whitefly Control (Pyriproxyfen), Pink Bollworm (Bifenthrin), Growth Promoter")
            st.warning(f"**Seed Total:** {6*acre} - {10*acre} KG")

        elif crop == "Dhan (Rice)":
            st.success("**Fertilizer (Khad):** 1 Bori DAP, 2 Bori Urea, Zinc Sulphate (Per Acre)")
            st.info("**Spray:** Stem Borer Control (Cartap), Blight Protection (Copper Oxychloride)")
            st.warning(f"**Seed Total:** {3*acre} - {5*acre} KG (Nursery)")

        elif crop == "Makai (Maize)":
            st.success("**Fertilizer (Khad):** 2 Bori DAP, 4 Bori Urea (3-4 installments), 1 Bori Potash")
            st.info("**Spray:** Fall Armyworm Control (Emamectin Benzoate), Growth Spray")
            st.warning(f"**Seed Total:** {8*acre} - {10*acre} KG")

    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHAR PLANNER ---
with tab3:
    st.write("### 🏠 Construction Estimate")
    # Previous code logic remains same
