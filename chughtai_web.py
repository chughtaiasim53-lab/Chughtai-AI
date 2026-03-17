import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# 2. Google Gemini API Setup
# Aapki API Key bilkul sahi hai
GOOGLE_API_KEY = "AIzaSyAajqHHlzBVwBj2QRrr1WxRYAD3lMPIOaQ"
genai.configure(api_key=GOOGLE_API_KEY)

# --- SIMPLE MODEL NAME ---
# Hum yahan sirf 'gemini-1.5-flash' use kar rahe hain
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Header
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai**")
st.markdown("---")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input
if prompt := st.chat_input("Yahan sawal likhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Simple Response call
            response = model.generate_content(f"Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. Jawab Roman Urdu mein dein: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Yeh line exact error batayegi
            st.error(f"Error Detail: {e}")
