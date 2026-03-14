import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import pandas as pd

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Digital Register", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 35px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 15px; border-radius: 10px; border-left: 5px solid #4facfe; margin-bottom: 10px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "kharcha_list" not in st.session_state: st.session_state.kharcha_list = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📜 Chat History")
    for chat in reversed(st.session_state.history):
        st.info(f"👉 {chat['u'][:30]}...")
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🚀 Chughtai AI - Digital Register</h1>', unsafe_allow_html=True)

tabs = st.tabs(["💬 Chat & News", "📝 Kharcha Register", "🌊 Tube-well Calc", "🌾 Mandi Rates"])

# --- TAB 1: CHAT ---
with tabs[0]:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            search_data = ""
            try:
                with DDGS() as ddgs:
                    r = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=2))
                    search_data = "\n".join([i['body'] for i in r])
            except: pass
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                          {"role": "user", "content": f"Data: {search_data}\n\nQ: {last_q}"}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            tts = gTTS(text=ans, lang='hi'); tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" controls autoplay></audio>', unsafe_allow_html=True)

# --- TAB 2: KHARCHA REGISTER ---
with tabs[1]:
    st.markdown("<div class='card'><h3>📝 Fasal ka Kharcha Likhein</h3>", unsafe_allow_html=True)
    item = st.text_input("Kis cheez par kharcha hua? (e.g. Beej, Diesel, Mazdoori)")
    amount = st.number_input("Kitne rupay?", min_value=0)
    if st.button("Kharcha Save Karein"):
        st.session_state.kharcha_list.append({"Item": item, "Amount": amount})
        st.success("Kharcha save ho gaya!")
    
    if st.session_state.kharcha_list:
        df = pd.DataFrame(st.session_state.kharcha_list)
        st.table(df)
        st.write(f"**Total Kharcha: Rs. {df['Amount'].sum()}**")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: TUBE-WELL CALCULATOR ---
with tabs[2]:
    st.markdown("<div class='card'><h3>🌊 Tube-well Diesel Calculator</h3>", unsafe_allow_html=True)
    hours = st.number_input("Tube-well kitne ghante chala?", min_value=0.0, value=1.0)
    diesel_rate = st.number_input("Diesel Rate (Rs/Litre):", value=280.0)
    consumption = st.number_input("Ek ghante mein kitna diesel (Litres)?", value=3.5)
    
    if st.button("Kharcha Nikalein"):
        total_litres = hours * consumption
        total_cost = total_litres * diesel_rate
        st.warning(f"Total Diesel: {total_litres} Litres")
        st.error(f"Total Kharcha: Rs. {int(total_cost)}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: MANDI RATES ---
with tabs[3]:
    st.markdown("### 🌾 Taza Mandi Rates (15 March 2026)")
    st.write("Gandum (Wheat): Rs. 4,380 | Kapas: Rs. 8,250 | Thum (G1): Rs. 14,000")
    st.info("💡 Tip: Rahim Yar Khan mandi mein aaj rate behtar hai.")
