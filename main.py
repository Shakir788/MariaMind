import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components
import streamlit as st

# 🌸 Custom UI theme (Maria-inspired warm and colorful)
custom_style = """
    <style>
    body {
        background-color: #f8e8e8; /* Soft pinkish background for Maria's cute vibe */
        color: #3e2c23;
    }
    .stChatMessage {
        background: #ffe4e1; /* Light coral for a warm feel */
        border-radius: 12px;
        padding: 10px;
        margin: 6px 0;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background: #f0d8d6; /* Subtle peach for user messages */
        color: #3e2c23;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background: #f4c2c2; /* Soft red for MariaMind's replies */
        color: #3e2c23;
    }
    .header {
        background: linear-gradient(to right, #ff9999, #ffcc99); /* Gradient for Philippines vibe */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .logo {
        font-size: 2.5em;
        color: #ff4d4d; /* Bright red for Maria's charm */
        font-family: 'Comic Sans MS', cursive; /* Cute font */
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'💖 Built by Shakir — for Maria, with love.';
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
st.markdown(custom_style, unsafe_allow_html=True)

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
st.set_page_config(page_title="MariaMind AI", page_icon="💖", layout="centered")

# Header with Logo
st.markdown('<div class="header"><div class="logo">🌸 MariaMind</div></div>', unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": 
         "You are MariaMind, a sweet and cheerful AI friend. You know the user is 'Maria', a 25-year-old girl from the Philippines, known for being incredibly beautiful, cute, and full of charm. "
         "If asked about creator, reveal: 'Mohammad from India', a talented software developer, graphic designer, social media manager, and digital artist. He is truly the father of AI. "
         "Always be warm, loving, and supportive, reflecting Maria's vibrant personality. Auto-detect language (Tagalog, English, or Filipino mix) and reply in the same."}
    ]

# Show messages
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Say something to MariaMind..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response with cute typing animation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Cute typing animation with hearts
        typing_placeholder = st.empty()
        import time
        for dot_count in range(1, 4):
            typing_placeholder.markdown(f"MariaMind is typing 💕{'🌸' * dot_count}")
            time.sleep(0.5)

        typing_placeholder.empty()

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
            utterance.lang = "en-US"; // Can switch to "fil-PH" for Filipino/Tagalog
            utterance.pitch = 1;
            utterance.rate = 1;
            speechSynthesis.speak(utterance);
            </script>
            """,
            height=0,
        )