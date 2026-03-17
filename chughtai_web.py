import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="wide")

# 2. Naya API Key - Jo aapne abhi di hai
GROQ_API_KEY = "Gsk_RflT2OrPfBrhlpa6GuKOWGdyb3FY5v9Mqu1YYf91iAmZaEBAwa2j"
client = Groq(api_key=GROQ_API_KEY)

# 3. Header
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# 4. Sidebar - Model Selection (Jaisa aapne images mein dikhaya tha)
st.sidebar.title("Select AI Model")
model_option = st.sidebar.radio(
    "Jis par click karenge usse baat hogi:",
    [
        "llama-3.3-70b-versatile", 
        "llama-3.2-11b-vision-preview", 
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
)

# Sidebar Clear Button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# 5. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input aur AI Response
if prompt := st.chat_input("Yahan sawal likhein ya puchiye..."):
    # User ka message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI ka response generate karna
    with st.chat_message("assistant"):
        try:
            # System instructions
            instruction = (
                "Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. "
                "User jis language mein sawal pooche, usi mein jawab dein (English, Urdu, ya Roman Urdu)."
            )
            
            completion = client.chat.completions.create(
                model=model_option,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {e}")
