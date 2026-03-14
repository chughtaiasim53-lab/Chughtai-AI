import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- Groq Setup ---
client = Groq(api_key="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")

st.set_page_config(page_title="Chughtai Smart AI", layout="centered")
st.title("🔍 Chughtai Smart Search")

# 1. YAHAN HIDAYAT LIKHNI HAIN (System Instructions)
instructions = """
Aap ek expert AI hain jo sirf SAHI aur LIVE data par yaqeen rakhta hai.
1. Agar user koi ghalat rate bataye (maslan Gold 5 lakh), to aap foran internet check karein.
2. Agar user ghalat hai, to usay pyar se Roman Urdu mein batayein: 'Asim bhai, internet par aaj ka sahi rate ye hai...'
3. Kabhi bhi user ki ghalat baat par 'Theek hai' mat kahein. 
4. Hamesha tola aur gram ka farq dhyan mein rakhein.
"""

aaj = datetime.date.today().strftime("%d %B %Y")

if prompt := st.chat_input("Mujhse sahi rates ya farming ki maloomat lein..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Internet se 100% sahi data check kiya ja raha hai..."):
                with DDGS() as ddgs:
                    # Deep Search query taaki ghalti na ho
                    search_query = f"{prompt} Pakistan official rates today {aaj} live"
                    results = [r for r in ddgs.text(search_query, max_results=5)]
                    search_context = "\n".join([f"Source: {r['body']}" for r in results])

            # 2. YAHAN 'instructions' KO SHAMIL KARNA HAI
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"{instructions} \n Aaj ki date {aaj} hai. Roman Urdu mein jawab dein. Internet Data: {search_context}"},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)

            # Voice
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
