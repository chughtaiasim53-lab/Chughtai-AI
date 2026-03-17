import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# 2. Google Gemini API Setup
# Aapki key bilkul sahi hai
GOOGLE_API_KEY = "AIzaSyAajqHHlzBVwBj2QRrr1WxRYAD3lMPIOaQ"
genai.configure(api_key=GOOGLE_API_KEY)

# --- STABLE MODEL SELECTION ---
# Maine yahan 'gemini-pro' kar diya hai jo har account par chalta hai
model = genai.GenerativeModel('gemini-pro')

# 3. App Header
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input aur AI Response
if prompt := st.chat_input("Yahan sawal likhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # AI ko instructions dena
            system_instruction = (
                "Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. "
                "User ki language (Urdu/Roman Urdu/English) mein jawab dein."
            )
            
            # Response generate karna
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar error aaye toh ye line screen par dikhayegi
            st.error(f"API Error: {e}")

# Sidebar
if st.sidebar.button("Clear History"):
    st.session_state.messages = []
    st.rerun()
