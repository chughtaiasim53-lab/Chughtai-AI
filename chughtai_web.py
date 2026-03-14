import streamlit as st
import google.generativeai as genai

# Aapki nikaali hui Nayi API Key
API_KEY = "AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE"

# Setup configuration
genai.configure(api_key=API_KEY)

# Page Setup
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="centered")

# Gemini style Dark Mode CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Chughtai AI Assistant")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Yahan kuch bhi search karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Ye 'gemini-1.5-flash' ka sabse stable tareeka hai
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar 1.5-flash masla kare to ye 'gemini-pro' par khud hi switch ho jayega
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response_alt = model_alt.generate_content(prompt)
                st.markdown(response_alt.text)
                st.session_state.messages.append({"role": "assistant", "content": response_alt.text})
            except Exception as e2:
                st.error(f"Technical Error: {str(e2)}")
