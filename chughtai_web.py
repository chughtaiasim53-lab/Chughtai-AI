import streamlit as st
import google.generativeai as genai

# Page Settings
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# Nayi API Key
GOOGLE_API_KEY = "AIzaSyDgq1gVcbvZ7zSZ00YbeEnb_nHsT4n68Q0"
genai.configure(api_key=GOOGLE_API_KEY)

# --- NEW STABLE MODEL CALL ---
# Flash model ko load karne ka naya aur fast tareeka
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # System instructions and generating response
            response = model.generate_content(f"Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. Jawab Roman Urdu mein dein: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar abhi bhi error aaye toh ye info help karegi
            st.error(f"Error: {e}")
            st.info("Mashwara: Streamlit Dashboard par '3 dots' par click karke Reboot karein.")

# Sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
