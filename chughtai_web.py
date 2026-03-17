import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# 2. Google Gemini API Setup
GOOGLE_API_KEY = "AIzaSyAajqHHlzBVwBj2QRrr1WxRYAD3lMPIOaQ"
genai.configure(api_key=GOOGLE_API_KEY)

# --- SIMPLE MODEL SELECTION ---
# Sirf 'gemini-pro' likhne se version ka masla khatam ho jata hai
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
            # Response generate karna
            # Hamne system instruction ko seedha prompt mein daal diya hai
            response = model.generate_content(f"Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. Jawab Roman Urdu ya English mein dein: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"API Error: {e}")
            st.info("Mashwara: Agar ye error na jaye, toh Streamlit Dashboard se app ko 'Reboot' karein.")

# Sidebar
if st.sidebar.button("Clear History"):
    st.session_state.messages = []
    st.rerun()
