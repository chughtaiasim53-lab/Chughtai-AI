import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

st.set_page_config(page_title="Chughtai AI - Professional Kisan", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #2ecc71; font-weight: bold; }
    .kisan-card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-top: 5px solid #2ecc71; }
    .calc-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌾 Chughtai AI - Accurate Kisan Calculator</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Chat & Search", "🚜 Accurate Calculator"])

with tab2:
    st.markdown("<div class='kisan-card'><h3>Zameen aur Fasal ki Tafseel</h3>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        # Ab ye 3.7 ya koi bhi point wala value sahi calculate karega
        acre = st.number_input("Zameen (Acres) likhein:", min_value=0.1, step=0.1, value=3.7)
    with col_b:
        fasal = st.selectbox("Fasal (Crop) select karein:", 
                            ["Gandum (Wheat)", "Rice (Basmati)", "Rice (Hybrid)", "Makka (Corn)", "Onion (Pyaz)", "Thomm (Garlic)"])
    
    if st.button("Mukammal Calculation Nikalein ✨"):
        # --- FIXED FORMULAS PER ACRE ---
        if fasal == "Gandum (Wheat)":
            beej_per_acre = 50; dap_per_acre = 1.0; urea_per_acre = 2.0; potash_per_acre = 0.5; zinc_per_acre = 2.0
        elif "Basmati" in fasal:
            beej_per_acre = 6; dap_per_acre = 1.0; urea_per_acre = 2.0; potash_per_acre = 0.5; zinc_per_acre = 5.0
        elif "Hybrid" in fasal:
            beej_per_acre = 9; dap_per_acre = 1.5; urea_per_acre = 3.0; potash_per_acre = 0.75; zinc_per_acre = 5.0
        elif fasal == "Thomm (Garlic)":
            beej_per_acre = 250; dap_per_acre = 2.0; urea_per_acre = 2.5; potash_per_acre = 1.0; zinc_per_acre = 3.0
        elif fasal == "Onion (Pyaz)":
            beej_per_acre = 4; dap_per_acre = 1.5; urea_per_acre = 2.0; potash_per_acre = 0.5; zinc_per_acre = 2.0
        elif fasal == "Makka (Corn)":
            beej_per_acre = 10; dap_per_acre = 1.5; urea_per_acre = 3.5; potash_per_acre = 1.0; zinc_per_acre = 3.0
        else:
            beej_per_acre = 40; dap_per_acre = 1.0; urea_per_acre = 2.0; potash_per_acre = 0.5; zinc_per_acre = 2.0

        # Final Multiplication with Acre (Precision 2 decimals)
        total_beej = round(acre * beej_per_acre, 2)
        total_dap = round(acre * dap_per_acre, 2)
        total_urea = round(acre * urea_per_acre, 2)
        total_potash = round(acre * potash_per_acre, 2)
        total_zinc = round(acre * zinc_per_acre, 2)

        st.markdown(f"### 📊 {acre} Acre {fasal} ki Accurate Report")
        st.markdown(f"<div class='calc-row'><span>🌱 **Total Beej (Seed):**</span> <span>{total_beej} KG</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Total DAP Khad:**</span> <span>{total_dap} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Total Urea Khad:**</span> <span>{total_urea} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Total Potash (SOP):**</span> <span>{total_potash} Bori</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='calc-row'><span>🧪 **Total Zinc (33%):**</span> <span>{total_zinc} KG</span></div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    # (Chat logic remain same as previous)
    pass
