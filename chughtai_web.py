import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

st.set_page_config(page_title="Chughtai AI - Professional", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #2ecc71; font-weight: bold; }
    .kisan-card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-top: 5px solid #2ecc71; }
    .calc-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN INTERFACE ---
st.markdown('<h1 class="main-title">🌾 Chughtai AI - Searching Fixed</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Search & Chat", "🚜 Precise Calculator"])

with tab2:
    st.markdown("<div class='kisan-card'><h3>Zameen ka Accurate Hisaab</h3>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        # 3.7 ya 2.5, ab har point par calculation sahi hogi
        acre = st.number_input("Zameen (Acres):", min_value=0.1, step=0.1, value=3.7)
    with col_b:
        fasal = st.selectbox("Fasal select karein:", ["Gandum (Wheat)", "Rice (Basmati)", "Makka (Corn)", "Thomm (Garlic)", "Onion (Pyaz)"])
    
    if st.button("Hisaab Lagayein ✨"):
        # Formulas fix kar diye hain
        rates = {
            "Gandum (Wheat)": {"beej": 50, "dap": 1, "urea": 2, "potash": 0.5},
            "Rice (Basmati)": {"beej": 6, "dap": 1, "urea": 2, "potash": 0.5},
            "Makka (Corn)": {"beej": 10, "dap": 1.5, "urea": 3.5, "potash": 1},
            "Thomm (Garlic)": {"beej": 250, "dap": 2, "urea": 2.5, "potash": 1},
            "Onion (Pyaz)": {"beej": 4, "dap": 1.5, "urea": 2, "potash": 0.5}
        }
        f = rates[fasal]
        st.success(f"### {acre} Acre {fasal} Report")
        st.write(f"🌱 **Beej (Seed):** {round(acre * f['beej'], 2)} KG")
        st.write(f"🧪 **DAP Khad:** {round(acre * f['dap'], 2)} Bori")
        st.write(f"🧪 **Urea Khad:** {round(acre * f['urea'], 2)} Bori")
        st.write(f"🧪 **Potash:** {round(acre * f['potash'], 2)} Bori")

with tab1:
    if prompt := st.chat_input("Aaj ka petrol ya sona rate poochen..."):
        st.session_state.history.append({"u": prompt, "b": "..."})
        
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            try:
                # --- FIXED SEARCH LOGIC ---
                search_text = ""
                with st.spinner("Searching Live Data..."):
                    try:
                        with DDGS() as ddgs:
                            # Search query mein 2026 lazmi dala hai
                            keywords = f"{prompt} Pakistan rate March 2026"
                            results = list(ddgs.text(keywords, max_results=3))
                            search_text = "\n".join([r['body'] for r in results])
                    except:
                        search_text = "Live search results temporarily unavailable."

                # Groq AI Response
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                        {"role": "user", "content": f"Context: {search_text}\n\nQuestion: {prompt}"}
                    ]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                
                # Manual Voice Control
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: Search nahi ho saki. API key check karein.")
