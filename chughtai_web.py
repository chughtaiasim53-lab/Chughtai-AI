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
st.set_page_config(page_title="Chughtai AI - Gemini Style", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #4facfe; font-weight: bold; margin-bottom: 20px; }
    .stChatInputContainer { position: fixed; bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN SCREEN ---
st.markdown('<h1 class="main-title">✨ Chughtai AI - Vision</h1>', unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("📜 History")
    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.rerun()
    for chat in reversed(st.session_state.history):
        st.write(f"👉 {chat['u'][:30]}...")

tab1, tab2, tab3 = st.tabs(["💬 Gemini Chat", "🚜 Kisan Markaz", "🏠 Ghar Planner"])

with tab1:
    # --- IMAGE UPLOAD (Like Gemini's Plus Icon) ---
    uploaded_pic = st.file_uploader("📸 Tasveer bhejain (Analytics ke liye):", type=["jpg", "png", "jpeg"])
    
    # Display Chat
    for chat in st.session_state.history:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.write(chat["b"])

    # Chat Input
    if prompt := st.chat_input("Yahan sawal puchiye..."):
        st.session_state.history.append({"u": prompt, "b": "Thinking..."})
        
        # --- ANALYSIS LOGIC ---
        with st.chat_message("assistant"):
            if uploaded_pic:
                # Agar tasveer hai to Vision Model use hoga
                with st.spinner("AI tasveer ko dekh raha hai..."):
                    img = Image.open(uploaded_pic)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    
                    res = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Sawal: {prompt}. Is tasveer ko dekhte hue Roman Urdu mein jawab dein."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                            ]
                        }]
                    )
                    ans = res.choices[0].message.content
            else:
                # Agar sirf text hai to Normal Chat + Search
                with st.spinner("Searching..."):
                    search_data = ""
                    try:
                        with DDGS() as ddgs:
                            r = list(ddgs.text(f"{prompt} Pakistan 2026", max_results=2))
                            search_data = "\n".join([i['body'] for i in r])
                    except: pass
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                                  {"role": "user", "content": f"Data: {search_context}\n\nQuestion: {prompt}"}]
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

# --- KISAN & GHAR TABS ---
with tab2:
    st.write("### 🚜 Kisan Calculator")
    acre = st.number_input("Acres:", value=3.7)
    if st.button("Hisaab"): st.success(f"DAP: {round(acre*1.2,1)} | Urea: {round(acre*2.5,1)}")

with tab3:
    st.write("### 🏠 Ghar Planner")
    marla = st.number_input("Marla:", value=5.0)
    if st.button("Estimate"): st.success(f"Intein: {int(marla*15000)} | Cement: {int(marla*110)}")
