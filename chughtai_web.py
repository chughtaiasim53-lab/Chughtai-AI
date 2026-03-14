import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- xAI (Grok) Setup ---
# API Key bilkul sahi format mein
client = OpenAI(
    api_key="xai-TL9zC1XlpRDTaOeGJXy5V4dAazIejYuFhmplmBlS4gnuO5yTI3VeVwi90SP2aqDwVU1uG6D320LBERBh",
    base_url="https://api.x.ai/v1",
)

st.set_page_config(page_title="Chughtai Grok Live", page_icon="🚀")
st.title("🚀 Chughtai xAI Grok Live")

aaj = datetime.date.today().strftime("%d %B %Y")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Aaj ka Petrol ya Gold rate puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Grok internet se data nikal raha hai..."):
                with DDGS() as ddgs:
                    # Specific query for Pakistan 2026
                    search_query = f"{prompt} Pakistan today {aaj} live"
                    results = [r for r in ddgs.text(search_query, max_results=3)]
                    search_data = "\n".join([r['body'] for r in results])

            # Grok Model Call - Model ka naam 'grok-2-1212' ya 'grok-beta' use karein
            completion = client.chat.completions.create(
                model="grok-beta", 
                messages=[
                    {"role": "system", "content": f"Aap Asim Chughtai ke AI hain. Aaj {aaj} hai. Roman Urdu mein jawab dein. Data: {search_data}"},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Voice Output
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            # Agar 400 error aaye to yahan wajah likhi aayegi
            st.error(f"Error Detail: {str(e)}")
        
