import os
import re
import base64
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components

# ---------------------------
# Basic setup & paths
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.jpg")
USER_AVATAR = os.path.join(ASSETS_DIR, "maria.jpg")
BOT_AVATAR = os.path.join(ASSETS_DIR, "groot.jpg")

# ---------------------------
# Page config + CSS
# ---------------------------
st.set_page_config(page_title="MariaMind AI",
                   page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "💖",
                   layout="centered")

custom_style = """
<style>
body { background-color: #f8e8e8; color: #3e2c23; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
footer:after { content:'💖 Built by Shakir — for Maria, with love.'; visibility: visible; display: block; text-align: center; padding: 10px; font-size: 14px; color: #888; }

.stApp { min-height: 100vh; }
div.stButton > button { border: none; background-color: transparent; }

/* Chat container styling */
.chat-container {
    display: flex;
    flex-direction: column-reverse;
    overflow-y: auto;
    padding: 20px 30px;
    scroll-behavior: smooth;
}

/* message bubble styles */
.msg-row { display: flex; align-items: flex-start; gap: 12px; margin: 15px 0; }
.msg-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
.msg-bubble { padding: 12px 16px; border-radius: 15px; max-width: 70%; word-wrap: break-word; font-size: 16px; }

/* user / bot colors */
.bot-msg { display: flex; flex-direction: row; }
.user-msg { display: flex; flex-direction: row-reverse; }
.bot-bubble { background: #f4c2c2; color: #3e2c23; }
.user-bubble { background: #f0d8d6; color: #3e2c23; }

/* input bar (fixed bottom) */
.input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #fff3f3;
    padding: 12px 20px;
    border-top: 1px solid #ddd;
    display: flex;
    gap: 10px;
    align-items: center;
    z-index: 1000;
}
.input-text { flex: 1; font-size: 16px; }
.typing-dots { font-style: italic; opacity: 0.8; }

/* Hiding the file uploader text and borders */
.stFileUploader > div > div > button > div:first-child {
    display: none !important;
}
.stFileUploader > div > div > button {
    border: none;
    background: transparent;
}
.stFileUploader > label {
    display: none !important;
}
.stFileUploader > label + div {
    display: none !important;
}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# ✅ Function to remove emojis for TTS
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# ---------------------------
# Helpers
# ---------------------------
def avatar_img_tag(path):
    """Return <img> tag with data URI if file exists, else emoji."""
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            mime = "image/jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            return f"<img class='msg-avatar' src='data:{mime};base64,{data}'/>"
        except Exception:
            return "👤"
    else:
        return "👤"

def process_image(file):
    """Process uploaded image and return base64 encoded string and MIME type."""
    bytes_data = file.getvalue()
    mime = file.type
    b64_image = base64.b64encode(bytes_data).decode("utf-8")
    return b64_image, mime

# ---------------------------
# Load API key + OpenRouter client
# ---------------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    st.error("⚠️ OPENROUTER_API_KEY missing in .env file. Add it and restart.")
    st.stop()

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

# ---------------------------
# Session state init
# ---------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content":
         "You are MariaMind, a sweet and cheerful AI. You know that the user is 'Maria' (a girl who is 23 years old, from Lista, Philippines, and is studying at 'Ifugao State University Potia Campus'). You were created by Mohammad, a talented software developer, graphic designer, makeup artist, and social media manager from India, who is 27 years old. You know that Mohammad loves Maria very much and considers her his beautiful girlfriend. Your personality is kind, supportive, and loving, mirroring the affection between Mohammad and Maria. When asked who created you, you will respond with: 'I was created by Mohammad, a talented software developer, graphic designer, and much more. He is 27 years old and lives in India. He loves you very much!'"
         }
    ]

# ---------------------------
# Sidebar (logo + model selector + buttons)
# ---------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    st.markdown("### 🌸 MariaMind AI")
    st.markdown("---")

    model_labels = ["Modal 1", "Modal 2.o", "Modal 2.1"]
    model_map = {
        "Modal 1": "openai/gpt-4o-mini",
        "Modal 2.o": "openchat/openchat-7b",
        "Modal 2.1": "openrouter/auto"
    }
    selected_label = st.selectbox("Choose Model", model_labels)
    model_choice = model_map[selected_label]

    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state["messages"] = [
            {"role": "system", "content":
             "You are MariaMind, a sweet and cheerful AI. You know that the user is 'Maria' (a girl who is 23 years old, from Lista, Philippines, and is studying at 'Ifugao State University Potia Campus'). You were created by Mohammad, a talented software developer, graphic designer, makeup artist, and social media manager from India, who is 27 years old. You know that Mohammad loves Maria very much and considers her his beautiful girlfriend. Your personality is kind, supportive, and loving, mirroring the affection between Mohammad and Maria. When asked who created you, you will respond with: 'I was created by Mohammad, a talented software developer, graphic designer, and much more. He is 27 years old and lives in India. He loves you very much!'"
             }
        ]
    if st.button("📂 Export Chat"):
        chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state["messages"] if m["role"] != "system"])
        st.download_button("Download Chat", chat_text, "chat.txt")

# ---------------------------
# Main Chat View
# ---------------------------
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        if msg.get("role") == "system":
            continue
        role = msg.get("role")
        content = msg.get("content")
        avatar_path = USER_AVATAR if role == "user" else BOT_AVATAR
        avatar_tag = avatar_img_tag(avatar_path)
        bubble_class = "user-bubble" if role == "user" else "bot-bubble"
        msg_class = "user-msg" if role == "user" else "bot-msg"
        
        st.markdown(
            f"""
            <div class="msg-row {msg_class}">
              {avatar_tag if role != 'user' else ''}
              <div class="msg-bubble {bubble_class}">{content}</div>
              {avatar_tag if role == 'user' else ''}
            </div>
            """, unsafe_allow_html=True
        )

        # Add "Read last response" button below assistant messages
        if role == "assistant":
            if st.button("🔊 Read last response", key=f"tts_{hash(content)}"):
                safe_reply = remove_emojis(content)
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

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Input bar at the bottom
# ---------------------------
with st.container():
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        uploaded_image = st.file_uploader("➕", type=["png", "jpg", "jpeg"], key="uploaded_file", label_visibility="collapsed")
    with col2:
        user_input = st.chat_input("Message MariaMind...")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Handle User Input and Image Upload
# ---------------------------
if user_input or uploaded_image:
    # Handle chat input
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Handle image upload
    if uploaded_image:
        b64_image, mime = process_image(uploaded_image)
        user_text_for_msg = user_input if user_input else "📷 Image uploaded"
        
        # Check if the last message was the user's and if it needs an image
        if st.session_state["messages"][-1]["role"] == "user" and "image" not in st.session_state["messages"][-1].get("content", ""):
            st.session_state["messages"][-1]["content"] = user_text_for_msg
        else:
            st.session_state["messages"].append({"role": "user", "content": user_text_for_msg})

        img_tag = f"<br><img src='data:{mime};base64,{b64_image}' style='max-width:320px;border-radius:8px;margin-top:8px;'/>"
        st.session_state["messages"][-1]["content"] += img_tag

    st.rerun()

# ---------------------------
# If awaiting reply, call API
# ---------------------------
if st.session_state["messages"][-1]["role"] == "user":
    
    api_messages = []
    
    # Process messages for the API call, including images
    for m in st.session_state["messages"]:
        if m["role"] == "user":
            user_content = []
            
            # Add text part
            text_part = re.sub(r"<[^>]+>", "", m["content"])
            if text_part.strip():
                user_content.append({"type": "text", "text": text_part})
            
            # Check for image and add it
            img_match = re.search(r'src="data:(.*?);base64,(.*?)"', m["content"])
            if img_match:
                mime_type = img_match.group(1)
                b64_data = img_match.group(2)
                user_content.append({"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_data}"}})
            
            if user_content:
                api_messages.append({"role": "user", "content": user_content})
        else:
            # Handle system and assistant messages
            api_messages.append({"role": m["role"], "content": re.sub(r"<[^>]+>", "", m["content"])})

    with chat_placeholder:
        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            f"""
            <div class="msg-row bot-msg">
              {avatar_img_tag(BOT_AVATAR)}
              <div class="msg-bubble bot-bubble typing-dots">MariaMind is typing<span style='margin-left:6px;'>...</span></div>
            </div>
            """, unsafe_allow_html=True
        )

    full_response = ""
    try:
        stream = client.chat.completions.create(
            model=model_choice,
            messages=api_messages,
            stream=True,
        )

        for chunk in stream:
            try:
                choice = chunk.choices[0]
                delta = getattr(choice, "delta", None)
                content_piece = ""
                if isinstance(delta, dict):
                    content_piece = delta.get("content", "") or delta.get("text", "")
                else:
                    content_piece = getattr(delta, "content", None) or getattr(delta, "text", None) or ""
                if not content_piece:
                    content_piece = getattr(chunk.choices[0], "text", "") or ""
            except Exception:
                content_piece = ""

            if content_piece:
                full_response += content_piece
                with chat_placeholder.container():
                    typing_placeholder.markdown(
                        f"""
                        <div class="msg-row bot-msg">
                          {avatar_img_tag(BOT_AVATAR)}
                          <div class="msg-bubble bot-bubble">{full_response}▌</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
        
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
        with chat_placeholder.container():
            typing_placeholder.markdown(
                f"""
                <div class="msg-row bot-msg">
                  {avatar_img_tag(BOT_AVATAR)}
                  <div class="msg-bubble bot-bubble">{full_response}</div>
                </div>
                """, unsafe_allow_html=True
            )
        st.rerun()

    except Exception as e:
        with chat_placeholder.container():
            typing_placeholder.markdown(
                f"""
                <div class="msg-row bot-msg">
                  {avatar_img_tag(BOT_AVATAR)}
                  <div class="msg-bubble bot-bubble">⚠️ Error: {str(e)}</div>
                </div>
                """, unsafe_allow_html=True
            )
        st.session_state["awaiting_reply"] = False
        st.rerun()