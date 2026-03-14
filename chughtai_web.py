import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Super App", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 15px; }
    .calc-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #333; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - 3D Pro</h1>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 Search & Chat", "🎨 3D Image Creator", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: AI CHAT & SEARCH ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Sawal puchiye ya Tasveer banwayein..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        
        # Image Logic in Chat
        if "tasveer" in last_q.lower() or "image" in last_q.lower() or "3d" in last_q.lower():
            with st.chat_message("assistant"):
                with st.spinner("🎨 3D Image bana raha hoon..."):
                    img_url = f"https://pollinations.ai/p/{last_q.replace(' ', '%20')}?width=1080&height=1080&model=flux&seed=42"
                    st.image(img_url, caption=f"Chughtai AI Result: {last_q}")
                    st.session_state.history[-1]["b"] = "Tasveer tayyar hai!"
        else:
            # Normal Search & Chat
            with st.chat_message("assistant"):
                with st.spinner("Searching Live Data..."):
                    try:
                        search_data = ""
                        with DDGS() as ddgs:
                            results = list(ddgs.text(f"{last_q} Pakistan 2026", max_results=3))
                            search_data = "\n".join([r['body'] for r in results])
                        
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                                {"role": "user", "content": f"Context: {search_data}\n\nQuestion: {last_q}"}
                            ]
                        )
                        ans = completion.choices[0].message.content
                        st.write(ans)
                        st.session_state.history[-1]["b"] = ans
                        
                        tts = gTTS(text=ans, lang='hi')
                        tts.save("v.mp3")
                        with open("v.mp3", "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()
                            st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
                    except:
                        st.error("Connection Error. Check internet.")

# --- TAB 2: 3D IMAGE GENERATOR ---
with tab2:
    st.markdown("<div class='card'><h3>🎨 3D Design Creator</h3>", unsafe_allow_html=True)
    img_prompt = st.text_input("Kya banana hai? (e.g. 3D Model of a modern house, 3D Tractor, 3D Garlic crop)")
    if st.button("Generate 3D Image ✨"):
        if img_prompt:
            with st.spinner("Creating..."):
                final_url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
                st.image(final_url)
                st.success("Aapki 3D tasveer tayyar hai!")

# --- TAB 3: KISAN CALCULATOR ---
with tab2:
    # (Purana kisan code mazeed accurate kar ke shamil hai niche wale tabs mein)
    pass

# --- TAB 3 & 4 (Kisan aur Ghar Planner ka sara purana logic shamil hai) ---
with tab3:
    st.markdown("<div class='card'><h3>🌾 Professional Kisan Calculator</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: acre = st.number_input("Zameen (Acres):", min_value=0.1, value=3.7, key="k_acre")
    with col2: fasal = st.selectbox("Fasal:", ["Gandum", "Rice (Basmati)", "Makka", "Thomm (Garlic)", "Onion"])
    
    if st.button("Hisaab 🚜"):
        f_map = {"Gandum":50, "Rice (Basmati)":7, "Makka":10, "Thomm (Garlic)":250, "Onion":4}
        st.success(f"### {acre} Acre Report:")
        st.write(f"🌱 Beej: {round(acre * f_map[fasal], 2)} KG")
        st.write(f"🧪 DAP: {round(acre * 1.2, 1)} Bori")
        st.write(f"🧪 Urea: {round(acre * 2.5, 1)} Bori")

with tab4:
    st.markdown("<div class='card'><h3>🏠 Tameerati Planner</h3>", unsafe_allow_html=True)
    t_type = st.selectbox("Kya banana hai?", ["Ghar (Marla)", "Sirf Kamra", "Sirf Kitchen", "Sirf Bathroom"])
    if st.button("Estimate 🏗️"):
        if t_type == "Sirf Kamra": st.write("🧱 Intein: 4500 | 🧪 Cement: 35 Bori")
        elif t_type == "Sirf Kitchen": st.write("🧱 Intein: 2200 | 🧪 Cement: 22 Bori")
        else: st.write("Apna size select karein.")
