import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
import datetime

# --- API Connection ---
client = Groq(api_key="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")

# --- UI STYLE ---
st.set_page_config(page_title="Chughtai AI - Kisan Dost", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #e3e3e3; }
    .main-title { font-size: 45px; text-align: center; color: #34a853; font-weight: bold; }
    .kisan-card { background-color: #1e1f20; padding: 25px; border-radius: 15px; border-top: 5px solid #34a853; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN INTERFACE ---
st.markdown('<h1 class="main-title">🌾 Chughtai AI - Kisan Markaz</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Chat & Search", "🚜 Advance Kisan Calculator"])

with tab2:
    st.markdown("<div class='kisan-card'><h3>Fasal ka Intekhab aur Hisaab</h3>", unsafe_allow_html=True)
    acre = st.number_input("Zameen (Acres) likhein:", min_value=0.5, step=0.5, value=2.5)
    
    # Nayi faslein shamil kar di hain
    fasal = st.selectbox("Fasal select karein:", 
                        ["Gandum (Wheat)", "Makka (Corn/Maize)", "Onion (Pyaz)", "Thomm (Garlic)", "Cotton"])
    
    if st.button("Report Banayein ✨"):
        # Specific Calculations for New Crops
        if fasal == "Makka (Corn/Maize)":
            beej = "8-10 KG (Hybrid)"
            dap = f"{acre * 1.5} Bori"
            urea = f"{acre * 3} Bori"
            tips = "Is fasal ko pani ki zyada zaroorat hoti hai, khas tor par jab dana ban raha ho."
        
        elif fasal == "Onion (Pyaz)":
            beej = "3-4 KG (Paneeri)"
            dap = f"{acre * 2} Bori"
            urea = f"{acre * 1.5} Bori"
            tips = "Pyaz ki fasal ke liye zameen ka bhur-bhura hona zaroori hai."
            
        elif fasal == "Thomm (Garlic)":
            beej = "200-250 KG (Desi/G1)"
            dap = f"{acre * 2} Bori"
            urea = f"{acre * 2} Bori"
            tips = "Thomm ke liye NPK ka istemal bulb barhane mein madad deta hai."
        
        else: # Default Wheat
            beej = f"{acre * 50} KG"
            dap = f"{acre * 1} Bori"
            urea = f"{acre * 2} Bori"
            tips = "Waqt par pani aur khad fasal ki paidawar barhati hai."

        st.success(f"### {acre} Acre {fasal} ki Mukammal Report:")
        st.write(f"🌱 **Beej ki Miqdar:** {beej}")
        st.write(f"🧪 **DAP Khad:** {dap}")
        st.write(f"🧪 **Urea Khad:** {urea}")
        st.info(f"💡 **Khas Mashwara:** {tips}")
        st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    # Existing Chat Logic
    for chat in st.session_state.chat_history:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.write(chat["bot"])

    if prompt := st.chat_input("Farming ya Market rates poochen..."):
        st.session_state.chat_history.append({"user": prompt, "bot": "Thinking..."})
        st.rerun()

# Processing (Same as previous)
if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Thinking...":
    last_prompt = st.session_state.chat_history[-1]["user"]
    with st.chat_message("assistant"):
        with st.spinner("Checking official data..."):
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(f"{last_prompt} Pakistan 2026", max_results=2)]
                context = "\n".join([r['body'] for r in results])
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Aap Chughtai AI hain. Roman Urdu mein jawab dein."},
                          {"role": "user", "content": last_prompt}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.session_state.chat_history[-1]["bot"] = ans
            
            # Voice control
            tts = gTTS(text=ans, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls></audio>', unsafe_allow_html=True)
