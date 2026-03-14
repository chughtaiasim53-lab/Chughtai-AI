import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- xAI (Grok) Setup ---
# Key: xai-TL9zC1XlpRDTaOeGJXy5V4dAazIejYuFhmplmBlS4gnuO5yTI3VeVwi90SP2aqDwVU1uG6D320LBERBh
client = OpenAI(
    api_key="xai-TL9zC1XlpRDTaOeGJXy5V4dAazIejYuFhmplmBlS4gnuO5yTI3VeVwi90SP2aqDwVU1uG6D320LBERBh",
    base_url="https://api.x.ai/v1",
)

# Page Layout
st.set_page_config(page_title="Chughtai Grok Live", page_icon="🚀", layout="centered")

# Gemini Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { color: #ffffff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Chughtai xAI Grok Live")

aaj = datetime.date.today().strftime("%d %B %Y")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Aaj ka Petrol ya Gold rate puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Grok internet se taza maloomat dhoond raha hai..."):
                # Live Search logic
                with DDGS() as ddgs:
                    search_query = f"{prompt} Pakistan today {aaj} live rates"
                    results = [r for r in ddgs.text(search_query, max_results=4)]
                    search_data = "\n".join([f"Source: {r['body']}" for r in results])

            # Grok (xAI) Response
            completion = client.chat.completions.create(
                model="grok-beta", 
                messages=[
                    {"role": "system", "content": f"Aap Asim Chughtai ke AI (Grok) hain. Aaj {aaj} hai. Is data se Roman Urdu mein jawab dein: {search_data}"},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Voice
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
