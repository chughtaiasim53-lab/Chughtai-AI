import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="wide")

# API Key
GROQ_API_KEY = "Gsk_Zay7aRdnI5ngkti8RQfhWGdyb3FY2qjEEFW4EzY2CAlZ1I1KdhJ9"
client = Groq(api_key=GROQ_API_KEY)

# Header Section
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# Sidebar - Model Selection (Jaisa photos mein tha)
st.sidebar.title("Select AI Model")
model_option = st.sidebar.radio(
    "Jis par click karenge usse baat hogi:",
    [
        "llama-3.3-70b-versatile", 
        "llama-3.2-11b-vision-preview", # Yeh image dekh sakta hai
        "mixtral-8x7b-32768", 
        "gemma2-9b-it"
    ]
)

# Image Upload Feature
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Image upload karein (Sirf Vision Model ke liye)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Yahan sawal likhein ya image ke baare mein puchein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # System Instruction
            sys_msg = "Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. User ki language mein jawab dein."
            
            # Agar image upload hai toh Vision Model use karein
            current_model = model_option
            if uploaded_file and "vision" in model_option:
                # Vision model logic yahan aayega
                st.info("Image analysis process ho rahi hai...")
            
            completion = client.chat.completions.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Error: {e}")

# Clear Button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()
