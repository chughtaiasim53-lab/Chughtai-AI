import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Setup ---
client = Groq(api_key="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")

# --- GEMINI STYLE ACCURATE INSTRUCTIONS ---
system_instructions = """
Role: Aap ek High-Accuracy AI Assistant hain, jaise Gemini.
Aapka Maqsad: User ko 100% sahi aur live data dena.

Rules:
1. User ki har baat par 'Theek hai' nahi kehna. Pehle internet search results ko check karein.
2. Agar user kahe ke 'Gold 5 lakh hai' aur internet kahe '2.8 lakh', to aap user ko foran correct karein.
3. Roman Urdu mein jawab dein aur rates ko hamesha **Bold** likhein.
4. Agar internet par kisi sawal ka jawab na miley, to kahein 'Mujhe iska live data nahi mila' bajaye ghalat jawab dene ke.
5. Har jawab ke end par 'Source: Internet Search' lazmi likhein.
"""

st.set_page_config(page_title="Chughtai Gemini-AI", layout="centered")
st.title("🤖 Chughtai Gemini-Style AI")

aaj = datetime.date.today().strftime("%d %B %Y")
st.write(f"📅 Aaj ki Date: **{aaj}** | Accuracy: **High**")

if prompt := st.chat_input("Sona, Petrol ya koi bhi sawal puchiye..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Gemini-style accuracy check ho raha hai..."):
                # 1. LIVE WEB SEARCH
                with DDGS() as ddgs:
                    # Specific query for Pakistan today
                    search_query = f"{prompt} Pakistan latest official data {aaj}"
                    results = [r for r in ddgs.text(search_query, max_results=5)]
                    live_data = "\n".join([f"Web Info: {r['body']}" for r in results])

            # 2. ACCURATE PROCESSING
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"{system_instructions}\nToday's Context: {live_data}\nDate: {aaj}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1 # Is se AI apni taraf se baatein nahi banata (High Accuracy)
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)

            # 3. VOICE
            tts = gTTS(text=answer, lang='hi')
            tts.save("accurate_voice.mp3")
            with open("accurate_voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"System Error: {str(e)}")
