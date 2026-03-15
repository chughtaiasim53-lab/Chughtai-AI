import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
from PIL import Image
import io
import os

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Super Farmer", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Vision</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("📜 History")
    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:30]}...")

tab1, tab2, tab3 = st.tabs(["💬 Gemini Chat", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: CHAT & VOICE ---
with tab1:
    uploaded_pic = st.file_uploader("📸 Tasveer bhejain (Analytics ke liye):", type=["jpg", "png", "jpeg"])
    
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Yahan sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        
        with st.chat_message("assistant"):
            ans = ""
            if uploaded_pic:
                with st.spinner("AI tasveer ko dekh raha hai..."):
                    img = Image.open(uploaded_pic)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    
                    res = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role": "user", "content": [
                            {"type": "text", "text": f"Sawal: {prompt}. Roman Urdu mein jawab dein."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                        ]}]
                    )
                    ans = res.choices[0].message.content
            else:
                with st.spinner("Searching..."):
                    search_data = ""
                    try:
                        with DDGS() as ddgs:
                            r = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                            search_data = "\n".join([i['body'] for i in r])
                    except: pass
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                                  {"role": "user", "content": f"Data: {search_data}\n\nQuestion: {prompt}"}]
                    )
                    ans = completion.choices[0].message.content
            
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            
            # Voice Output Fix
            try:
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64_audio = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64_audio}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- TAB 2: KISAN MARKAZ (UPDATED WITH ALL CROPS) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Advanced Kisan Calculator</h3>", unsafe_allow_html=True)
    
    crop = st.selectbox("Fasal Chunain (Crop Selection):", 
                        ["Thomm (Garlic)", "Cotton (Kapas)", "Gandum (Wheat)", "Onion (Piyaz)", "Rice (Simple)", "Rice (Hybrid)"])
    
    acre = st.number_input("Zameen (Acres):", value=1.0, min_value=0.1)
    
    if st.button("Hisaab Lagayein"):
        st.markdown(f"#### 📋 {crop} Report for {acre} Acre")
        
        if crop == "Thomm (Garlic)":
            st.success(f"🧄 **DAP:** {round(acre*2.5, 1)} Bori | **Urea:** {round(acre*2.0, 1)} Bori | **Potash:** {round(acre*2.0, 1)} Bori")
            st.info(f"💡 **Seed (Beej):** {int(acre*800)} - 1000 KG")

        elif crop == "Cotton (Kapas)":
            st.success(f"🌿 **DAP:** {round(acre*1.5, 1)} Bori | **Urea:** {round(acre*3.0, 1)} Bori | **Potash:** {round(acre*1.0, 1)} Bori")

        elif crop == "Gandum (Wheat)":
            st.success(f"🌾 **DAP:** {round(acre*1.2, 1)} Bori | **Urea:** {round(acre*2.5, 1)} Bori")

        elif crop == "Onion (Piyaz)":
            st.success(f"🧅 **DAP:** {round(acre*2.0, 1)} Bori | **Urea:** {round(acre*1.5, 1)} Bori | **Potash:** {round(acre*1.5, 1)} Bori")

        elif crop == "Rice (Simple)":
            st.success(f"🍚 **DAP:** {round(acre*1.0, 1)} Bori | **Urea:** {round(acre*2.0, 1)} Bori")

        elif crop == "Rice (Hybrid)":
            st.success(f"🍚⚡ **DAP:** {round(acre*1.5, 1)} Bori | **Urea:** {round(acre*3.0, 1)} Bori | **Zinc:** 5-10 KG")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHAR PLANNER ---
with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar & Kamra Planner</h3>", unsafe_allow_html=True)
    m_type = st.selectbox("Kya tameer karna hai?", ["Pura Ghar", "Akela Kamra (12x14)", "Akela Kitchen", "Akela Bathroom"])
    
    if m_type == "Pura Ghar":
        m_size = st.number_input("Marla:", value=5.0)
        if st.button("Estimate"):
            st.success(f"🏠 {m_size} Marla: {int(m_size*18000)} Intein, {int(m_size*125)} Cement, {round(m_size*0.85, 2)} Ton Sarya")
    else:
        if st.button(f"{m_type} Estimate"):
            if "Kamra" in m_type: st.success("6,500 Intein, 45 Cement, 0.35 Ton Sarya")
            elif "Kitchen" in m_type: st.success("3,200 Intein, 25 Cement, 0.15 Ton Sarya")
            else: st.success("1,800 Intein, 15 Cement")
    st.markdown("</div>", unsafe_allow_html=True)
