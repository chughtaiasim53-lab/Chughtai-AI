import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖", layout="wide")

# 2. API Key aur Client Setup (Isse error theek ho jayega)
GROQ_API_KEY = "Gsk_Zay7aRdnI5ngkti8RQfhWGdyb3FY2qjEEFW4EzY2CAlZ1I1KdhJ9"
client = Groq(api_key=GROQ_API_KEY)

# 3. Header Section
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# 4. Sidebar - Model Selection
st.sidebar.title("Select AI Model")
model_option = st.sidebar.radio(
    "Jis par click karenge usse baat hogi:",
    ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview", "mixtral-8x7b-32768"]
)

# 5. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input aur AI Response
if prompt := st.chat_input("Yahan sawal likhein..."):
    # User ka message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI ka response
    with st.chat_message("assistant"):
        try:
            # System instructions
            instruction = "Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. User ki language follow karein."
            
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

# Sidebar mein clear button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
