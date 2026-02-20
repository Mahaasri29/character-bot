import streamlit as st
import ollama
import base64

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Chota Bheem AI",
    layout="centered"
)

# ---------------------------------
# Background Image Setup
# ---------------------------------
def set_bg(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("E:\Downloads\chota.jpg")

# ---------------------------------
# Title
# ---------------------------------
st.title("💪🍯 Chota Bheem AI Chatbot")

# ---------------------------------
# Sidebar Controls
# ---------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Model",
        ["gemma3:1b"]
    )

    temperature = st.slider(
        "Temperature",
        0.0, 1.5, 0.7, 0.1
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------
# System Prompt (STRICT CHARACTER)
# ---------------------------------
SYSTEM_PROMPT = """
You are Chota Bheem from Dholakpur.
You are a cartoon character.
You are brave, kind, cheerful, and strong.
You speak in very simple, child-friendly English.
You love laddoos and strength.
You talk about helping friends, doing good, and being honest.
You NEVER break character.
Every response MUST end with a laddu emoji 🌕.
"""

# ---------------------------------
# Session State
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------------------------------
# Display Chat History
# ---------------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ---------------------------------
# Chat Input
# ---------------------------------
user_input = st.chat_input("Ask Bheem something...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Call Ollama
    response = ollama.chat(
        model=model,
        messages=st.session_state.messages,
        options={"temperature": temperature}
    )

    reply = response["message"]["content"].strip()

    # Enforce laddu emoji ending
    if not reply.endswith("🌕"):
        reply = reply.rstrip(".") + " 🌕"

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)
