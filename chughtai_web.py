import streamlit as st
import google.generativeai as genai

# Website ki basic settings - Robot icon hata kar Google AI jaisa Sparkle (✨) laga diya hai
st.set_page_config(page_title="CHUGHTAI AI", page_icon="✨", layout="wide")

# ==========================================
# 3D aur Modern UI ke liye Custom CSS
# ==========================================
custom_css = """
<style>
/* Main Background - Dark 3D Gradient */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* 3D Glassmorphism Chat Boxes */
.stChatMessage {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 25px !important;
    padding: 20px !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

/* Hover karne par 3D Pop-out effect */
.stChatMessage:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7) !important;
}

/* 3D Input Box (Sawal likhne wali jagah) */
.stChatInputContainer {
    border-radius: 25px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6) !important;
    background: rgba(0, 0, 0, 0.7) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 5px !important;
}

/* Sidebar ka 3D aur Gradient Design */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141e30, #243b55) !important;
    box-shadow: 5px 0 20px rgba(0,0,0,0.6) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}

/* Headings ka 3D Shadow */
h1, h2, h3 {
    text-shadow: 3px 3px 6px rgba(0,0,0,0.6) !important;
    color: #00d2ff !important;
}

/* Text boxes (API Key daalne ki jagah) ki 3D styling */
div[data-baseweb="input"] > div {
    background-color: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6), 0 2px 5px rgba(255,255,255,0.1) !important;
    color: white !important;
}

/* Dropdown Menu ki 3D styling */
div[data-baseweb="select"] > div {
    background-color: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.5), 0 2px 5px rgba(255,255,255,0.1) !important;
    color: white !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# Asal App ka Code
# ==========================================
st.title("✨ CHUGHTAI AI")
st.markdown("### Sirf Gemini AI ke sath ek behtareen 3D tajarba!")

# Sidebar mein API Keys ka setup (Aapki key pehle se daal di hai)
st.sidebar.header("🔑 API Key Setup")
st.sidebar.markdown("Aapki Gemini API Key code mein pehle se set kar di gayi hai. Aapko ab menu mein kuch type nahi karna parega!")

# User ki di hui key ko default value bana diya gaya hai
gemini_key = st.sidebar.text_input("Google Gemini API Key", value="AIzaSyBD7VSUFI1GxKns8jmbMSxe8mwW6u-loHc", type="password")

st.sidebar.markdown("---")
# AI Model select karne ka option
model_choice = st.sidebar.selectbox("🧠 Model Select Karein", 
                                    ["Gemini 1.5 Flash (Tez)", "Gemini 1.5 Pro (Smart)"])

# Chat history save rakhne ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat screen par dikhane ke liye
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User ka sawal likhne ki jagah
prompt = st.chat_input("CHUGHTAI AI se apna sawal poochein...")

if prompt:
    # User ka sawal screen par dikhayein
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        if not gemini_key:
            st.error("⚠️ API Key mojood nahi hai.")
        else:
            # Gemini API ko configure karna
            genai.configure(api_key=gemini_key)
            
            # User ki pasand ke mutabiq model select karna
            if model_choice == "Gemini 1.5 Flash (Tez)":
                model = genai.GenerativeModel('gemini-1.5-flash')
            else:
                model = genai.GenerativeModel('gemini-1.5-pro')
                
            # Jawab generate karna
            response = model.generate_content(prompt)
            msg = response.text
            
            # Jawab ko screen par dikhana
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

    except Exception as e:
        st.error(f"❌ Koi masla aa gaya. Barae meharbani check karein ke API Key sahi hai ya nahi. Error: {e}")
