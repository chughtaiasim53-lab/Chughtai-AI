import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- Groq Setup ---
# Aapki Key: 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
client = Groq(api_key="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")

# --- UI Design (Premium Beauty) ---
st.set_page_config(page_title="Chughtai All-Search AI", page_icon="🔍", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stChatInputContainer { border-radius: 20px !important; border: 2px solid #4facfe !important; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 15px; border-left: 5px solid #4facfe; }
    h1 { background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-size: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Chughtai Smart Search")

aaj = datetime.date.today().strftime("%d %B %Y")
st.write(f"✨ Welcome **Asim Chughtai**! Aaj ki date hai: **{aaj}**")

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Searching Anything)
if prompt := st.chat_input("Farming, Gold rates, ya kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Internet se behtareen maloomat dhoondi ja rahi hain..."):
                # 1. LIVE SEARCH (Har Topic ke liye)
                with DDGS() as ddgs:
                    search_query = f"{prompt} Pakistan today {aaj} latest updates"
                    results = [r for r in ddgs.text(search_query, max_results=4)]
                    search_context = "\n".join([f"Info: {r['body']}" for r in results])

            # 2. GROQ PROCESSING (Llama 3.3 - Super Fast)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Aap Asim Chughtai ke expert Assistant hain. Aaj {aaj} hai. Internet data ka nichor Roman Urdu mein behtareen tareeqe se dein. Data: {search_context}"},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # 3. VOICE OUTPUT
            tts = gTTS(text=answer, lang='hi')
            tts.save("search_voice.mp3")
            with open("search_voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Masla Aa Gaya: {str(e)}")
