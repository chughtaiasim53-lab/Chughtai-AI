import streamlit as st
from groq import Groq
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="wide")

# API Key (securely from environment)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY environment variable not set!")
    st.stop()

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
            
            # Current model selection
            current_model = model_option
            
            # Prepare messages
            messages = [
                {"role": "system", "content": sys_msg},
            ]
            
            # Agar image upload hai aur vision model selected hai
            if uploaded_file and "vision" in current_model:
                st.info("📸 Image analysis process ho rahi hai...")
                
                # Read and encode image to base64
                image_data = uploaded_file.read()
                base64_image = base64.standard_b64encode(image_data).decode("utf-8")
                
                # Determine image media type
                image_type = uploaded_file.type  # e.g., "image/jpeg"
                
                # Add image to message content
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_type,
                                "data": base64_image
                            }
                        }
                    ]
                })
            else:
                # Regular text message
                messages.append({"role": "user", "content": prompt})
            
            # Call Groq API
            completion = client.chat.completions.create(
                model=current_model,
                messages=messages,
                max_tokens=1024
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Clear Button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()