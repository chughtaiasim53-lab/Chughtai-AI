import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime
import requests

# --- API Connection ---
client = Groq(api_key="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")

# --- Interface Styling ---
st.set_page_config(page_title="Chughtai Super AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4facfe; color: white; }
    .stTextInput>div>div>input { border-radius: 20px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3137,#2e3137); color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Chughtai Super Accurate AI")

# --- Sidebar for History ---
if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("📜 Chat History")
for h in st.session_state.history:
    st.sidebar.write(f"👉 {h[:30]}...")

# --- Main Logic ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Image Generator")
    img_prompt = st.text_input("Kya tasveer banaun? (e.g. Beautiful Village)")
    if st.button("Generate Image"):
        if img_prompt:
            with st.spinner("Tasveer ban rahi hai..."):
                # Pollinations.ai use kar rahe hain (No Limit/No API Key needed)
                img_url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '%20')}?width=1080&height=1080&seed=42&model=flux"
                st.image(img_url, caption=f"Result for: {img_prompt}")
                st.session_state.history.append(f"Image: {img_prompt}")

with col2:
    st.subheader("💬 Chat & Search")
    # Voice to Text (Browser based approach)
    st.info("💡 Tip: Mobile keyboard ka Mic button use karein bolne ke liye, ye sabse best chalta hai.")
    prompt = st.chat_input("Gold, Petrol ya koi bhi sawal...")

if prompt:
    st.session_state.history.append(f"User: {prompt}")
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching..."):
                with DDGS() as ddgs:
                    r = [res for res in ddgs.text(f"{prompt} Pakistan 2026", max_results=3)]
                    context = "\n".join([res['body'] for res in r])
            
            aaj = datetime.date.today().strftime("%d %B %Y")
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Aap Asim Chughtai ke AI hain. Roman Urdu mein jawab dein. Date: {aaj}. Data: {context}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            ans = completion.choices[0].message.content
            st.markdown(ans)
            
            # Voice Output
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")
