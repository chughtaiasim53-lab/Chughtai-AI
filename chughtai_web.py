import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# 2. Google Gemini Setup
# Aapki Nayi Key bilkul sahi hai
GOOGLE_API_KEY = "AIzaSyDgq1gVcbvZ7zSZ00YbeEnb_nHsT4n68Q0"
genai.configure(api_key=GOOGLE_API_KEY)

# --- NEW MODEL CALL ---
# Hum yahan 'gemini-1.5-flash-latest' use karenge jo 404 error nahi deta
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    # Agar Flash na chale toh 'gemini-pro' try karein
    model = genai.GenerativeModel('gemini-pro')

# 3. UI Section
st.title("🤖 Chughtai AI")
st.markdown("**Asim Chughtai son Qadir Dad**")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan sawal likhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # AI Response Generation
            response = model.generate_content(f"Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar abhi bhi error aaye toh exact detail dikhayega
            st.error(f"Response Error: {e}")
            st.info("Mashwara: Google AI Studio mein ja kar 'Safety Settings' off karke dekhein.")

# Sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
