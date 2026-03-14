import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import time

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Professional", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    .calc-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HISTORY) ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Markaz</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("📜 Purani Baatein")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    # History ko reverse mein dikhana taaki naya sawal upar ho
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:30]}...")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["💬 Chat & Live News", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: CHAT & LIVE NEWS ---
with tab1:
    # Chat display
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Input Box
    if prompt := st.chat_input("Aaj ki news ya koi sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            with st.spinner("Internet se maloomat le raha hoon..."):
                search_context = ""
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f"{last_q} Pakistan news 2026", max_results=2))
                        search_context = "\n".join([r['body'] for r in results])
                except:
                    search_context = "Search slow hai, AI purani data use karega."

                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Aaj 15 March 2026 hai."},
                            {"role": "user", "content": f"Data: {search_context}\n\nQuestion: {last_q}"}
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
                        st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
                except:
                    st.error("Server busy hai, thori dair baad koshish karein.")

# --- TAB 2: KISAN CALCULATOR ---
with tab2:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator (3.7 Acre Formula)</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", value=3.7, step=0.1)
    if st.button("Hisaab Nikalein 🚜"):
        dap = round(acre * 1.2, 1)
        urea = round(acre * 2.5, 1)
        st.success(f"### {acre} Acre Report:")
        st.write(f"🧪 DAP Khad: {dap} Bori")
        st.write(f"🧪 Urea Khad: {urea} Bori")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHAR PLANNER ---
with tab3:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    marla = st.number_input("Marla Size:", value=5.0)
    if st.button("Estimate Check Karein 🏗️"):
        intein = int(marla * 15000)
        cement = int(marla * 110)
        st.success(f"### {marla} Marla Estimate:")
        st.write(f"🧱 Intein: {intein}")
        st.write(f"🧪 Cement: {cement} Bori")
    st.markdown("</div>", unsafe_allow_html=True)
