import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime
import random

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - 3D Pro", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 40px; text-align: center; color: #4facfe; font-weight: bold; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Super Fast Fix</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🎨 3D Image (FIXED)", "🚜 Kisan", "🏠 Ghar"])

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
            except:
                st.error("Error.")

# --- TAB 2: 3D IMAGE GENERATOR (NEW DISPLAY LOGIC) ---
with tab2:
    st.markdown("<div class='card'><h3>🎨 3D Design Creator</h3>", unsafe_allow_html=True)
    img_prompt = st.text_input("Kya banana hai? (e.g. Modern 3D House Design)")
    
    if st.button("Generate Image ✨"):
        if img_prompt:
            with st.spinner("AI Tasveer bana raha hai..."):
                # Naya display tareeka (Caching hatane ke liye seed aur random numbers)
                seed = random.randint(1, 100000)
                clean_prompt = img_prompt.replace(" ", "%20")
                img_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&seed={seed}&model=flux"
                
                # HTML ke zariye display karna (Zyada stable hai)
                st.markdown(f"""
                    <div style="text-align: center;">
                        <img src="{img_url}" width="100%" style="border-radius: 10px; border: 2px solid #4facfe;">
                        <br><br>
                        <a href="{img_url}" target="_blank" style="background-color: #4facfe; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 Download Tasveer</a>
                    </div>
                """, unsafe_allow_html=True)
                st.success("Aapki 3D tasveer oper nazar aa rahi hai!")

# --- TAB 3 & 4 (Shortened for space, keep your previous accurate logic here) ---
with tab3:
    st.write("Kisan Calculator tayyar hai.")
with tab4:
    st.write("Ghar Planner tayyar hai.")
