import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime
import requests

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - 3D Pro", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - 3D Pro</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Search & Chat", "🎨 3D Image Creator", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

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
            with st.spinner("Searching..."):
                try:
                    search_data = ""
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=2))
                        search_data = "\n".join([r['body'] for r in results])
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                                  {"role": "user", "content": f"Context: {search_data}\n\nQuestion: {last_q}"}]
                    )
                    ans = completion.choices[0].message.content
                    st.write(ans)
                    st.session_state.history[-1]["b"] = ans
                except:
                    st.error("Error in connection.")

# --- TAB 2: 3D IMAGE GENERATOR (FIXED) ---
with tab2:
    st.markdown("<div class='card'><h3>🎨 3D Design Creator</h3>", unsafe_allow_html=True)
    img_prompt = st.text_input("Kya banana hai? (e.g. 3D Model of a modern house)")
    
    if st.button("Generate 3D Image ✨"):
        if img_prompt:
            with st.spinner("Tasveer ban rahi hai, thora intezar karein..."):
                # Naya strong URL format
                encoded_prompt = img_prompt.replace(" ", "%20")
                img_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={datetime.datetime.now().second}"
                
                # Direct display check
                st.image(img_url, use_column_width=True)
                st.success("Aapki 3D tasveer tayyar hai!")
                st.markdown(f"🔗 [Tasveer Download Karein]({img_url})")

# --- TAB 3: KISAN CALCULATOR ---
with tab3:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", min_value=0.1, value=3.7)
    fasal = st.selectbox("Fasal:", ["Gandum", "Rice", "Makka", "Garlic", "Onion"])
    if st.button("Hisaab 🚜"):
        st.success(f"{acre} Acre {fasal} Report: DAP {round(acre*1.2,1)} Bori, Urea {round(acre*2.5,1)} Bori.")

# --- TAB 4: GHAR PLANNER ---
with tab4:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    m = st.number_input("Marla:", value=5.0)
    if st.button("Estimate 🏗️"):
        st.success(f"{m} Marla Estimate: {int(m*15000)} Intein, {int(m*110)} Bori Cement.")
