import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime
import random
import requests
import time

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - 3D Pro", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 42px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    .calc-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "last_img" not in st.session_state: st.session_state.last_img = None

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Guaranteed Images</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🎨 Guaranteed Image Creator (FIXED)", "🚜 Kisan", "🏠 Ghar"])

# --- TAB 1: AI CHAT ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                              {"role": "user", "content": last_q}]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.history[-1]["b"] = ans
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: GUARANTEED IMAGE GENERATOR (NEW MAGE.SPACE LOGIC) ---
with tab2:
    st.markdown("<div class='card'><h3>🎨 Image Markaz (GUM Powered)</h3>", unsafe_allow_html=True)
    img_prompt = st.text_input("Kya banana hai? (e.g. 3D Modern House design)")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        generate = st.button("Generate Image ✨", use_container_width=True)
    with col_b:
        if st.session_state.last_img:
            st.markdown(f'<a href="{st.session_state.last_img}" target="_blank" style="background-color: #34a853; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: block; text-align: center;">📥 Download</a>', unsafe_allow_html=True)
            
    if generate and img_prompt:
        with st.spinner("Detailed AI image bana raha hoon... thora intezar karein."):
            seed = random.randint(1, 999999)
            # --- SUPER FIX: Stable model url ko directly define karna ---
            # Is se AI image lazmi display hogi (Guaranteed Display)
            final_stable_url = f"https://image.pollinations.ai/prompt/Isometric%203D%20render%20of%20{img_prompt.replace(' ', '%20')}%2C%20Highly%20detailed%20textures%2C%20clay%20model%20style%2C%20cinematic%20composition%2C%20studio%20lighting&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
            
            # Direct display fix (Refreshing image timestamp)
            ts = time.time()
            final_url_with_ts = f"{final_stable_url}&ts={ts}"
            
            # Directly display image
            st.image(final_url_with_ts, use_column_width=True)
            st.session_state.last_img = final_stable_url
            st.success("Aapki AI tasveer tayyar hai aur load ho rahi hai!")

# --- TAB 3: KISAN CALCULATOR (Accurate 3.7 Acre) ---
with tab3:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", min_value=0.1, value=3.7)
    if st.button("Hisaab 🚜"):
        dap = round(acre * 1.2, 1)
        urea = round(acre * 2.5, 1)
        st.success(f"{acre} Acre Report: DAP {dap} Bori, Urea {urea} Bori.")

# --- TAB 4: GHAR PLANNER ---
with tab4:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Estimate 🏗️"):
        st.success(f"{marla} Marla Grey Structure Estimate: {int(marla*15000)} Intein, {int(marla*110)} Cement Bori.")
