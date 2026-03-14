import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - History Fix", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HISTORY INITIALIZATION) ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR (History yahan nazar aayegi) ---
with st.sidebar:
    st.markdown("<h2 style='color: #4facfe;'>📜 Purani Baatein</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Sab Khatam Karein"):
        st.session_state.history = []
        st.rerun()
    
    st.write("---")
    
    # History list dikhane ka pakka tareeka
    if not st.session_state.history:
        st.info("Abhi koi history nahi hai. Pehla sawal puchiye!")
    else:
        for i, chat in enumerate(reversed(st.session_state.history)):
            # Chota sa box banakar purane sawal dikhana
            st.markdown(f"**{i+1}.** {chat['u'][:35]}...")
            st.write("---")

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Pro</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Chat & News", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: CHAT ---
with tab1:
    # Chat display (Screen par purani chat dikhana)
    for chat in st.session_state.history:
        with st.chat_message("user"):
            st.write(chat["u"])
        with st.chat_message("assistant"):
            st.write(chat["b"])

    # Input Box
    if prompt := st.chat_input("Yahan sawal puchiye..."):
        # Sawal ko history mein save karna
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    # AI Response Logic
    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Internet se dhoond raha hoon..."):
                search_context = ""
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f"{last_q} Pakistan news 2026", max_results=2))
                        search_context = "\n".join([r['body'] for r in results])
                except: pass

                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                            {"role": "user", "content": f"Data: {search_context}\n\nSawal: {last_q}"}
                        ]
                    )
                    ans = completion.choices[0].message.content
                    st.write(ans)
                    st.session_state.history[-1]["b"] = ans
                    
                    # Voice Output
                    tts = gTTS(text=ans, lang='hi')
                    tts.save("v.mp3")
                    with open("v.mp3", "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
                except:
                    st.error("Server Busy!")

# --- TABS 2 & 3 ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3></div>", unsafe_allow_html=True)
    a = st.number_input("Zameen (Acres):", value=3.7, key="k_acre")
    if st.button("Hisaab 🚜"):
        st.success(f"{a} Acre Report: DAP {round(a*1.2, 1)} Bori, Urea {round(a*2.5, 1)} Bori.")

with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3></div>", unsafe_allow_html=True)
    m = st.number_input("Marla:", value=5.0, key="m_size")
    if st.button("Estimate 🏗️"):
        st.success(f"{m} Marla Estimate: {int(m*15000)} Intein, {int(m*110)} Bori Cement.")
