import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os
import time

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE (Gemini Style & Round Interface) ---
st.set_page_config(page_title="Chughtai AI - Modern", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    
    /* Round Title & Cards */
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 25px; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 25px; border: 1px solid #333; margin-bottom: 20px; }
    
    /* Round Chat Bubbles */
    [data-testid="stChatMessage"] { border-radius: 25px; padding: 15px; margin-bottom: 10px; border: 1px solid #333; }
    [data-testid="stChatMessageContent"] { font-size: 16px; }
    
    /* Round Input Box */
    .stChatInputContainer textarea { border-radius: 30px !important; border: 1px solid #4facfe !important; padding: 10px 20px !important; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: #1e1f20; border-radius: 20px; padding: 10px 20px; color: white; border: none; }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">🚜 Chughtai AI</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Modern Chat", "🌾 Agri Plan", "🏠 Build Plan"])

# --- TAB 1: CHAT (With Streaming & Round UI) ---
with tab1:
    # Pehli chat history dikhana
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Naya sawal
    if prompt := st.chat_input("Fasal ya bemari ke bare mein puchiye..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        # AI Response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 16 March 2026."},
                          {"role": "user", "content": prompt}]
            )
            ans = completion.choices[0].message.content
            
            # Streaming Effect (Typewriter)
            for chunk in ans.split():
                full_response += chunk + " "
                time.sleep(0.05)
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            
            # Save to history
            st.session_state.history.append({"u": prompt, "b": full_response})
            
            # Voice Output
            try:
                tts = gTTS(text=full_response, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                os.remove("v.mp3")
            except: pass

# --- TAB 2: KISAN CALCULATOR (Round UI) ---
with tab2:
    st.markdown("<div class='card'><h3>🚜 Per Acre Full Management Plan</h3>", unsafe_allow_html=True)
    crop = st.selectbox("Fasal Chunain:", ["Lehsan (Garlic)", "Gandum (Wheat)", "Kapas (Cotton)", "Dhan (Rice)", "Makai (Maize)"])
    acre = st.number_input("Zameen (Acres):", value=2.5, min_value=0.1, step=0.1)
    
    if st.button("Mukammal Plan Dekhein"):
        st.markdown(f"### 📋 {crop} Management for {acre} Acre")
        if crop == "Lehsan (Garlic)":
            st.success(f"**Seed Total:** {200*acre} - {250*acre} KG")
            st.info("**Spray:** Fungicide (Agi-M), Weedicide, Amino Acid")
        elif crop == "Gandum (Wheat)":
            st.success(f"**Seed Total:** {40*acre} - {50*acre} KG")
        # Baqi faslon ka logic aapke pas pehle se hai...
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHAR PLANNER ---
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### 🏠 Construction Estimate")
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Calculate"):
        st.success(f"Intein: {int(marla*18000)} | Cement: {int(marla*125)} Bori")
    st.markdown("</div>", unsafe_allow_html=True)
