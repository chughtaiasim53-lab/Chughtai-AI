import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
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
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">🚜 Chughtai AI - Kisan Markaz</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 AI Chat & Voice", "🌾 Seed & Khad Calculator", "🏠 Ghar Planner"])

# --- TAB 1: CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        with st.chat_message("assistant"):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": prompt}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            
            # Voice Fix
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: KISAN CALCULATOR (UPDATED SEED DATA) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Per Acre Seed & Fertilizer Requirement</h3>", unsafe_allow_html=True)
    
    crop = st.selectbox("Fasal Chunain:", 
                        ["Gandum (Wheat)", "Kapas (Cotton)", "Makai (Maize)", "Dhan (Rice/Munji)", 
                         "Moong Phali (Peanut)", "Sarson/Canola", "Lehsan (Garlic)"])
    
    acre = st.number_input("Zameen (Acres):", value=1.0, min_value=0.1)
    
    if st.button("Hisaab Check Karein"):
        st.markdown(f"#### 📊 {crop} Report for {acre} Acre")
        
        # Seed and Fertilizer Logic based on your data
        if crop == "Gandum (Wheat)":
            seed, dap, urea = "40-50 KG", 1.25, 2.5
        elif crop == "Kapas (Cotton)":
            seed, dap, urea = "6-10 KG (Delinted)", 1.5, 3.0
        elif crop == "Makai (Maize)":
            seed, dap, urea = "8-10 KG", 2.0, 4.0
        elif crop == "Dhan (Rice/Munji)":
            seed, dap, urea = "3-5 KG (Nursery)", 1.0, 2.0
        elif crop == "Moong Phali (Peanut)":
            seed, dap, urea = "35-40 KG (Baghair chilke)", 1.0, 0.5
        elif crop == "Sarson/Canola":
            seed, dap, urea = "1.5-2 KG", 1.0, 1.5
        elif crop == "Lehsan (Garlic)":
            seed, dap, urea = "200-250 KG (Turiyan)", 2.5, 2.0

        st.success(f"🌱 **Seed (Beej):** {seed} per acre (Total: {acre} acre ke liye check karein)")
        st.info(f"🧱 **DAP:** {round(acre*dap, 1)} Bori | **Urea:** {round(acre*urea, 1)} Bori")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHAR PLANNER ---
with tab3:
    st.write("### 🏠 Construction Estimate")
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Calculate"):
        st.write(f"Intein: {int(marla*18000)} | Cement: {int(marla*125)}")
