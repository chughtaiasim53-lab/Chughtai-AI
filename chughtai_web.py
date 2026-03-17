import streamlit as st
import google.generativeai as genai

# 1. Page Configuration (App Title aur Look)
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="centered")

# 2. Google Gemini API Setup
# Aapki di hui key yahan set kar di gayi hai
GOOGLE_API_KEY = "AIzaSyAajqHHlzBVwBj2QRrr1WxRYAD3lMPIOaQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Model initialize karna
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. App Header
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# 4. Chat History (Taki AI purani baatein yaad rakhe)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input aur AI Response logic
if prompt := st.chat_input("Yahan sawal likhein..."):
    # User ka message display karna
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI ka jawab nikalna
    with st.chat_message("assistant"):
        try:
            # AI ko instructions dena (System Prompt)
            system_instruction = (
                "Aap Chughtai AI hain. Aapke owner Asim Chughtai son Qadir Dad hain. "
                "Aap kisanon aur aam logon ki madad ke liye banaye gaye hain. "
                "User jis language mein sawal pooche (Urdu, Roman Urdu, ya English), "
                "usi mein mukammal aur behtareen jawab dein."
            )
            
            # AI se response mangna (System instruction + User ka sawal)
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            ai_text = response.text
            
            st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            
        except Exception as e:
            st.error(f"API Error: {e}")

# Sidebar mein clear button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
