import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Kisan Dost", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; }
    .kisan-card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #34a853; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.title("📜 Purani Baatein")
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()
    for chat in reversed(st.session_state.chat_history):
        st.write(f"👉 {chat['user'][:30]}...")

# --- MAIN INTERFACE ---
st.markdown('<h1 class="main-title">🌾 Chughtai AI - Kisan Dost</h1>', unsafe_allow_html=True)

# --- NEW: FARMING CALCULATOR TAB ---
tab1, tab2 = st.tabs(["💬 Chat & Search", "🚜 Kisan Calculator"])

with tab2:
    st.markdown("<div class='kisan-card'><h3>Zameen ka Hisaab-Kitab</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres mein) likhein:", min_value=0.5, step=0.5, value=2.5)
    crop = st.selectbox("Fasal (Crop) select karein:", ["Gandum (Wheat)", "Kapaas (Cotton)", "Ganna (Sugarcane)", "Amrood (Guava)"])
    
    if st.button("Hisaab Lagayein ✨"):
        # Calculation Logic for Pakistan Farming
        beej = acre * 50 # 50kg per acre for wheat
        dap = acre * 1 # 1 bag per acre
        urea = acre * 2 # 2 bags per acre
        solar_req = "5kW to 10kW" if acre > 2 else "3kW"
        
        st.success(f"### {acre} Acre {crop} ke liye Report:")
        st.write(f"📦 **Beej (Seed):** Takreeban {beej} KG")
        st.write(f"🧪 **DAP Khad:** {dap} Bori")
        st.write(f"🧪 **Urea Khad:** {urea} Bori")
        st.write(f"☀️ **Solar System:** Aapko kam az kam {solar_req} ka setup chahiye.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    # Display Chat
    for chat in st.session_state.chat_history:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.write(chat["bot"])

    # Chat Input
    if prompt := st.chat_input("Gold rate, Weather ya Farming sawal puchiye..."):
        st.session_state.chat_history.append({"user": prompt, "bot": "Thinking..."})
        
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching Live Data..."):
                    with DDGS() as ddgs:
                        r = [res for res in ddgs.text(f"{prompt} Pakistan rates March 2026", max_results=2)]
                        context = "\n".join([res['body'] for res in r])
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Aap kisanon ke hamdard hain."},
                        {"role": "user", "content": prompt}
                    ]
                )
                ans = completion.choices[0].message.content
                st.write(ans)
                st.session_state.chat_history[-1]["bot"] = ans
                
                # Manual Voice Control
                tts = gTTS(text=ans, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
            except:
                st.error("Error occurred. Try again.")
