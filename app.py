import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components
import streamlit as st

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'💖 Built by Shakir — for Artchen, with love.';
        visibility: visible;
        display: block;
        position: relative;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #888;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Function to remove emojis for TTS
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # chinese symbols
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ OPENROUTER_API_KEY missing in .env file")
    st.stop()

# OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Streamlit setup
st.set_page_config(page_title="Artia AI", page_icon="💜", layout="centered")
st.title("💜 Artia – Your AI Companion")

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": 
         "You are Artia, a sweet AI friend. You know that the user is 'Artchen' (a girl from the Philippines). "
         "If asked about creator, reveal: 'Mohammad from India' he is a talented software developer, "
         "graphic designer, social media manager, and digital artist. "
         "He is truly the father of AI. Always be warm, loving, and supportive."}
    ]

# Show messages
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Say something to Artia..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        stream = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=st.session_state["messages"],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# 🎙️ Voice input (browser recording only - demo)
components.html(
    """
    <button onclick="recordAndSend()">🎤 Record Voice (5s)</button>
    <script>
    async function recordAndSend() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];

            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'audio/webm' });
                alert("🎤 Voice recorded! (Now connect to STT API if needed)");
            };

            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 5000);
        } catch (err) {
            alert("Mic permission denied or not available.");
        }
    }
    </script>
    """,
    height=100,
)

# 🔊 Voice output (TTS using browser speechSynthesis)
if st.button("🔊 Read last response"):
    if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "assistant":
        last_reply = st.session_state["messages"][-1]["content"]
        safe_reply = remove_emojis(last_reply)
        components.html(
            f"""
            <script>
            const utterance = new SpeechSynthesisUtterance({safe_reply!r});
            utterance.lang = "en-US";
            utterance.pitch = 1;
            utterance.rate = 1;
            speechSynthesis.speak(utterance);
            </script>
            """,
            height=0,
        )
