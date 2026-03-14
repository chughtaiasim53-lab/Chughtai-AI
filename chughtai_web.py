import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import base64
import datetime
import requests # Image generation ke liye

# --- API Connections ---
GROQ_API_KEY = "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"
# HUGGINGFACE KEY (Tasveer banane ke liye - Ye muft hai)
HF_API_KEY = "hf_YhQJpUjVpEFrLgGfYKkKxXfNzDdBbCd" # Test key, aap apni bhi laga sakte hain

client = Groq(api_key=GROQ_API_KEY)

# --- Modern Interface Style ---
st.set_page_config(page_title="Chughtai Super AI", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #3e3e5e; margin-bottom: 10px; }
    .stButton>button { background-color: #4facfe; color: white; border-radius: 20px; }
    .stTextInput>div>div>input { border-radius: 20px; border: 1px solid #4facfe; }
    .sidebar-content { background-color: #161b22; padding: 20px; border-radius: 15px; }
    h1 { background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Chughtai Super Voice & Image AI")

# --- 1. CHAT HISTORY (Sidebar) ---
st.sidebar.title("📜 Chat History")
if "messages" not in st.session_state:
    st.session_state.messages = []

# History dikhane ka tareeqa
for i, msg in enumerate(st.session_state.messages):
    st.sidebar.markdown(f"**{msg['role'].capitalize()}:** {msg['content'][:50]}...")

# --- 2. MODERN INTERFACE (Main Screen) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 🎙️ Bol kar sawal puchiye:")
    # Mic button screen ke beech mein
    audio_input = mic_recorder(start_prompt="Recording Shuru Karein", stop_prompt="Rokein", key='recorder')

    st.write("### 🎨 Tasveer Banane ke liye Likhain:")
    image_prompt = st.text_input("Roman Urdu mein description dein (e.g. Aik haseen mazar)...", key="img_prompt")
    generate_btn = st.button("Generate Image")

with col2:
    st.write("### 💬 Chat/Search Input:")
    prompt = st.chat_input("Gold, Petrol, etc... type karein")

# --- Logic for Processing Inputs ---
final_prompt = ""
aaj = datetime.date.today().strftime("%d %B %Y")

# Voice input filter
if audio_input and 'text' in audio_input:
    final_prompt = audio_input['text']
    st.info(f"🎤 Record hua: {final_prompt}")

# Text input filter
if prompt:
    final_prompt = prompt

# --- 3. IMAGE GENERATION LOGIC ---
if generate_btn and image_prompt:
    st.session_state.messages.append({"role": "user", "content": f"Image generated for: {image_prompt}"})
    with st.spinner("Tasveer banayi ja rahi hai..."):
        try:
            # Hugging Face API call for free image generation
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            response = requests.post(API_URL, headers=headers, json={"inputs": f"{image_prompt}, photorealistic, detailed"})
            
            if response.status_code == 200:
                st.image(response.content, caption=f"Generated for: {image_prompt}")
            else:
                st.error("Tasveer nahi ban saki, shayad description ghalat hai ya API limit khatam hai.")
        except Exception as e:
            st.error(f"Image Error: {str(e)}")

# --- 4. CHAT LOGIC WITH HISTORY & WEB SEARCH ---
if final_prompt:
    # History mein user ka sawal add karna
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.chat_message("user").markdown(final_prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Internet scan ho raha hai..."):
                with DDGS() as ddgs:
                    # Specific query for Pakistan today
                    search_query = f"{final_prompt} Pakistan official data March 2026"
                    results = [r for r in ddgs.text(search_query, max_results=3)]
                    live_context = "\n".join([r['body'] for r in results])

            # Groq call (Llama 3)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Aap Asim Chughtai ke Super AI hain. Roman Urdu mein jawab dein. Date: {aaj}. Web Data: {live_context}"},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0 
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            # History mein AI ka jawab add karna
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Voice Output
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Chat Error: {str(e)}")
