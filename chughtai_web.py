import streamlit as st
from groq import Groq

# --- Setup ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="Chughtai AI", page_icon="🚀", layout="centered")

# --- CSS for Modern Dark Look ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { text-align: center; font-family: 'Google Sans'; }
    .stChatInput { position: fixed; bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Session States
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 1. Login Screen (With Balloons) ---
if not st.session_state.user_name:
    st.markdown("<br><br><h1>Chughtai AI</h1>", unsafe_allow_html=True)
    name_input = st.text_input("Apna naam likhein shuru karne ke liye:", placeholder="Asim Chughtai...")
    
    if name_input:
        st.session_state.user_name = name_input
        st.balloons() # 🎉 Celebration
        st.success(f"Welcome {name_input}!")
        st.rerun()

else:
    # --- 2. Sidebar Mein Extra Features ---
    with st.sidebar:
        st.title("Chughtai AI Tools")
        st.info(f"User: {st.session_state.user_name}")
        
        # Audio Input Feature
        st.subheader("🎤 Voice Chat")
        audio_file = st.audio_input("Record karein")
        if audio_file:
            st.write("Audio received! (Isse text mein badalne ke liye Whisper API chahiye hogi)")

        # Camera Input Feature
        st.subheader("📸 Camera")
        img_file = st.camera_input("Photo khinchein")
        if img_file:
            st.image(img_file, caption="Aapki Photo", use_container_width=True)
            st.toast("Nice photo!")

    # --- 3. Main Chat Interface ---
    st.markdown(f"### Hello, {st.session_state.user_name} ✨")
    
    # Purani chat dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Yahan kuch bhi poochein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            try:
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": f"Your name is Chughtai AI. You are a genius AI assistant talking to {st.session_state.user_name}."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Connection Error! Check internet.")

    # Reset Chat Button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
