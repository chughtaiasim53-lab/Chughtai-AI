import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
from PIL import Image
import io

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Vision & Analytics", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-left: 5px solid #4facfe; margin-bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HISTORY RE-ADDED) ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Analytics Center</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("📜 Chat History")
    if st.button("🗑️ Clear All"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:30]}...")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & Live News", "📸 AI Analytics (Vision)", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: CHAT & NEWS ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Aaj ki news, rates ya koi sawal..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        st.rerun()

    if st.session_state.history and st.session_state.history[-1]["b"] == "Thinking...":
        last_q = st.session_state.history[-1]["u"]
        with st.chat_message("assistant"):
            search_context = ""
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(f"{last_q} Pakistan news 2026", max_results=2))
                    search_context = "\n".join([r['body'] for r in results])
            except: pass

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein. Date: 15 March 2026."},
                          {"role": "user", "content": f"Context: {search_context}\n\nQuestion: {last_q}"}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.history[-1]["b"] = ans
            
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)

# --- TAB 2: AI ANALYTICS (VISION) ---
with tab2:
    st.markdown("<div class='card'><h3>📸 Tasveer Analyze Karein (AI Vision)</h3>", unsafe_allow_html=True)
    pic = st.file_uploader("Koi bhi tasveer (Fasal, Naksha, ya Item) upload karein:", type=["jpg", "png", "jpeg"])
    
    if pic:
        img = Image.open(pic)
        st.image(img, caption="Aapki Tasveer", use_container_width=True)
        
        if st.button("AI Analytics Chalaein 🔍"):
            with st.spinner("AI tasveer ki gehrai ko dekh raha hai..."):
                try:
                    # Convert to base64 for Vision model
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()

                    # Llama 3.2 Vision Model ka istemal
                    res = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Is tasveer ko mukammal analyze karein aur Roman Urdu mein batayein ke ye kya hai, is mein kya khas baat hai, aur agar koi masla hai to uska hal kya hai?"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                            ]
                        }]
                    )
                    st.success("### Analytics Report:")
                    st.write(res.choices[0].message.content)
                except:
                    st.error("Vision API busy hai. Dobara koshish karein.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: KISAN (3.7 Acre Formula) ---
with tab3:
    st.markdown("<div class='card'><h3>🌾 Kisan Markaz</h3>", unsafe_allow_html=True)
    a = st.number_input("Zameen (Acres):", value=3.7, key="ka_acre")
    if st.button("Hisaab 🚜"):
        st.success(f"{a} Acre Report: DAP {round(a*1.2, 1)} Bori, Urea {round(a*2.5, 1)} Bori.")

# --- TAB 4: GHAR PLANNER ---
with tab4:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    m = st.number_input("Marla:", value=5.0, key="ma_size")
    if st.button("Estimate 🏗️"):
        st.success(f"{m} Marla Estimate: {int(m*15000)} Intein, {int(m*110)} Cement Bori.")
