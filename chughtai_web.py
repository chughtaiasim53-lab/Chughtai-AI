import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from duckduckgo_search import DDGS 
import datetime
import base64

# --- Gemini API Setup ---
# Agar aapne Secrets mein key dali hai to wahan se uthayega
try:
    api_key = st.secrets["AIzaSyDv72uFDyJi2oIh9OIcJ-2EMtDQrc64jKI"]
except:
    # Testing ke liye aapki purani key
    api_key = "AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE"

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Page Layout (Gemini Style)
st.set_page_config(page_title="Chughtai Gemini Live", page_icon="✨", layout="centered")

# Aaj ki date
aaj_ki_date = datetime.date.today().strftime("%d %B %Y")

# Custom CSS for Gemini Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stChatMessage { border-radius: 20px; margin-bottom: 12px; padding: 15px; }
    h1 { color: #ffffff; font-family: 'Google Sans', sans-serif; text-align: center; font-weight: 600; }
    .stTextInput input { border-radius: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Chughtai Gemini Live AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.info(f"Assalam-o-Alaikum Asim! Aaj {aaj_ki_date} hai. Main Gold, Petrol aur Live News dhoond kar bata sakta hoon.")

# Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Yahan kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Google Search se taza maloomat li ja rahi hain..."):
                # DuckDuckGo Search for Accuracy
                search_query = f"{prompt} Pakistan today live rates {aaj_ki_date}"
                search_data = ""
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(search_query, max_results=5)]
                    search_data = "\n".join([f"Source: {r['title']}\nData: {r['body']}" for r in results])

            # Gemini Response Generation
            full_prompt = f"""
            System Instruction: Aap Asim Chughtai ke banaye huye Gemini AI hain.
            Aaj ki Date: {aaj_ki_date}.
            
            Aapne niche diye gaye Internet data ko use karke user ko bilkul sahi jawab dena hai.
            Data: {search_data}
            
            Rules:
            1. Roman Urdu mein jawab dein.
            2. Rates (Gold/Petrol/Dollar) ko hamesha **Bold** mein likhein.
            3. Agar data March 2026 ka nahi hai, to keh dein ke 'Taza rates abhi update nahi huye'.
            """
            
            response = model.generate_content([full_prompt, prompt])
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LISTEN OPTION (Voice) ---
            tts = gTTS(text=answer, lang='hi', slow=False)
            tts.save("gemini_voice.mp3")
            
            # Autoplay audio logic
            with open("gemini_voice.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay="true"></audio>', unsafe_allow_html=True)
            
            st.audio("gemini_voice.mp3")
            
        except Exception as e:
            st.error(f"Masla aa gaya hai: {str(e)}")
