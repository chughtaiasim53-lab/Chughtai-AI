import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# OpenAI API Key (Yahan apni 'sk-...' wali key dalein)
client = OpenAI(api_key="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")

st.set_page_config(page_title="Chughtai ChatGPT Live", page_icon="🤖")

st.title("🚀 Chughtai Smart AI (ChatGPT)")

# Aaj ki date
aaj = datetime.date.today().strftime("%d %B %Y")

if prompt := st.chat_input("Aaj ka Petrol ya Gold rate puchiye..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 1. Internet se Live Search karna
            with st.spinner("Google se taza maloomat li ja rahi hain..."):
                with DDGS() as ddgs:
                    # Pakistan specific search
                    search_query = f"{prompt} Pakistan today {aaj} live rates"
                    results = [r for r in ddgs.text(search_query, max_results=3)]
                    context = "\n".join([r['body'] for r in results])

            # 2. ChatGPT (GPT-4o) ko Search results dikhana
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Yeh sasta aur tez model hai
                messages=[
                    {"role": "system", "content": f"Aaj ki date {aaj} hai. Is internet data ko use karke Roman Urdu mein jawab dein: {context}"},
                    {"role": "user", "content": prompt}
                ]
            )
            ai_text = response.choices[0].message.content
            st.markdown(ai_text)

            # 3. Audio (Insaani Awaaz)
            tts = gTTS(text=ai_text, lang='hi')
            tts.save("voice.mp3")
            
            # Autoplay audio
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
            st.audio("voice.mp3")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
