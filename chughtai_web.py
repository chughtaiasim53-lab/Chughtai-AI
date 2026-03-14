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
st.set_page_config(page_title="Chughtai AI - Pro", layout="wide")

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
st.markdown('<h1 class="main-title">✨ Chughtai AI - Vision Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("📜 Purani Baatein")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:30]}...")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & News", "📸 Image Analysis", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

# --- TAB 1: CHAT & NEWS ---
with tab1:
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    if prompt := st.chat_input("Aaj ki news ya koi sawal..."):
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
            
            # Voice Output
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'**🔊 Suniye:** <audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)

# --- TAB 2: IMAGE ANALYSIS (NEW FUNCTION) ---
with tab2:
    st.markdown("<div class='card'><h3>📸 Tasveer ki Pehchan (Vision)</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Fasal ya kide ki photo upload karein:", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Tasveer ko Analyze Karein 🔍"):
            with st.spinner("AI tasveer ko dekh raha hai..."):
                # Groq Vision Model Use karna
                try:
                    # Tasveer ko base64 mein convert karna
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    completion = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Is tasveer ko dekh kar Roman Urdu mein batayein ke ye kya hai aur agar koi masla (disease/pest) hai to uska hal batayein."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                                ]
                            }
                        ]
                    )
                    analysis = completion.choices[0].message.content
                    st.success("### AI Analysis:")
                    st.write(analysis)
                except Exception as e:
                    st.error("Vision model filhal busy hai. Dobara koshish karein.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: KISAN (Accurate) ---
with tab3:
    st.markdown("<div class='card'><h3>🌾 Kisan Calculator</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres):", value=3.7, key="k_acre")
    if st.button("Hisaab 🚜"):
        st.success(f"{acre} Acre Report: DAP {round(acre*1.2, 1)} Bori, Urea {round(acre*2.5, 1)} Bori.")

# --- TAB 4: GHAR ---
with tab4:
    st.markdown("<div class='card'><h3>🏠 Ghar Planner</h3>", unsafe_allow_html=True)
    m = st.number_input("Marla:", value=5.0, key="m_size")
    if st.button("Estimate 🏗️"):
        st.success(f"{m} Marla Estimate: {int(m*15000)} Intein, {int(m*110)} Bori Cement.")
