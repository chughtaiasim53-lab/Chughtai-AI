import streamlit as st
import google.generativeai as genai

# Sahi API Key (Wahi jo aapne nikaali thi)
API_KEY = "AIzaSyAskNQNR0gzJWbjbGPREmRStVgHi5wiHdE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Chughtai AI", page_icon="✨")

# Naya Tareeka: Model list check karke sahi model uthana
try:
    # Google ab 'models/gemini-1.5-flash-latest' ko pasand karta hai
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("✨ Chughtai AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Response generate karna
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar error aaye to technical details ke bajaye asaan msg dikhaye
            st.error("Technical Issue: Google ka naya update aaya hai. Refresh karke dubara try karein.")
            st.write(f"Error Detail: {str(e)}")
