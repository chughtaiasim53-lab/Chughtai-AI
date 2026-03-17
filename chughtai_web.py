import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Chughtai AI", page_icon="🤖")

# 2. Google Gemini API Setup (Nayi Key ke saath)
# Aapki di hui Nayi Key yahan set kar di gayi hai
GOOGLE_API_KEY = "AIzaSyDgq1gVcbvZ7zSZ00YbeEnb_nHsT4n68Q0"
genai.configure(api_key=GOOGLE_API_KEY)

# --- AUTO MODEL SELECTION ---
# Yeh hissa check karega ke aapki key ke liye kaunsa model available hai
@st.cache_resource
def load_model():
    try:
        # Pehle Flash try karein (Fast)
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        # Agar Flash na chale toh Pro (Stable)
        return genai.GenerativeModel('gemini-pro')

model = load_model()

# 3. App Header
st.title("🤖 Chughtai AI")
st.markdown(f"**Asim Chughtai son Qadir Dad**")
st.markdown("---")

# 4. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input aur AI Response
if prompt := st.chat_input("Yahan sawal likhein..."):
    # User message display
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response generation
    with st.chat_message("assistant"):
        try:
            # System instructions
            system_prompt = (
                "Aap Chughtai AI hain. Owner Asim Chughtai son Qadir Dad hain. "
                "User ki language (Urdu/Roman Urdu/English) mein behtareen jawab dein."
            )
            
            response = model.generate_content(f"{system_prompt}\n\nUser Question: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar abhi bhi koi masla ho toh exact error dikhayega
            st.error(f"Technical Error: {e}")
            st.info("Mashwara: GitHub par requirements.txt check karein.")

# Sidebar - Clear History button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
