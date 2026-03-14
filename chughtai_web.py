import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- Interface Styling ---
st.set_page_config(page_title="Chughtai Gemini-AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 2px solid #4facfe; margin-bottom: 10px; }
    h1 { background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Chughtai Accurate AI")

aaj = datetime.date.today().strftime("%d %B %Y")
st.write(f"📅 Aaj ki Date: **{aaj}** | Status: **Gemini Accuracy Active**")

# --- RULES FOR THE AI ---
system_rules = f"""
Role: Aap Asim Chughtai ke Smart Assistant hain.
Hidayat: 
1. Aap hamesha LIVE data check karenge. 
2. Agar Asim kahe ke Petrol 200 ya Gold 10 lakh hai, to aapne foran internet se verify karke sahi rate batana hai.
3. Petrol ka sahi rate 321.17 PKR hai (March 2026).
4. Sona (Gold) 24K ka rate takreeban 2,84,500 PKR hai.
5. Kabhi bhi 'Theek hai' mat kahein agar data ghalat ho. Roman Urdu mein jawab dein.
"""

if prompt := st.chat_input("Gold, Petrol ya koi bhi rate puchiye..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Checking official sources..."):
                with DDGS() as ddgs:
                    # Sirf 2026 ke taza results ke liye query
                    search_query = f"{prompt} Pakistan latest official price March 2026"
                    results = [r for r in ddgs.text(search_query, max_results=3)]
                    live_context = "\n".join([r['body'] for r in results])

            # Processing with Temperature 0 (Matlab bilkul serious mode)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"{system_rules}\nWeb Data: {live_context}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0 
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)

            # Voice Output
            tts = gTTS(text=answer, lang='hi')
            tts.save("voice.mp3")
            with open("voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
