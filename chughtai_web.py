from gtts import gTTS
import os
import base64

def speak_text(text):
    # Text ko audio mein convert karna
    tts = gTTS(text=text, lang='ur') # 'ur' for Urdu ya 'hi' for Hindi
    tts.save("response.mp3")
    
    # Audio file ko Streamlit mein play karne ke liye convert karna
    with open("response.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    
    # File delete karna taaki space na bhare
    os.remove("response.mp3")

# --- Chat Logic mein aise use karein ---
if prompt := st.chat_input("Message Chughtai AI..."):
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        # Jawab likhne ke baad AI bolega bhi
        speak_text(response.text)
