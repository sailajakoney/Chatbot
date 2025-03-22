import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set Streamlit UI configuration
st.set_page_config(page_title="Gemini AI Chatbot", layout="wide")

# JSON file to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history from JSON file
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat history to JSON file
def save_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(messages, file, indent=4)

# Custom CSS for styling chat UI
st.markdown(
    """
    <style>
        /* Background and font settings */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
        /* Chat container */
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }
        /* User messages */
        .user-bubble {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            margin-bottom: 10px;
            text-align: left;
            margin-left: auto;
            display: block;
        }
        /* AI messages */
        .ai-bubble {
            background-color: #ECECEC;
            color: black;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            margin-bottom: 10px;
            margin-right: auto;
            display: block;
        }
        /* Chat alignment */
        .user-container { text-align: right; }
        .ai-container { text-align: left; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for instructions
with st.sidebar:
    st.title("🛠 How to Use")
    st.write("1. Type a message in the chat box below.")
    st.write("2. Press **Enter** to send. ")
    st.write("3. Wait for the AI's response. ")
    st.write("4. The conversation history is saved.")

# Title
st.markdown("<h1 style='text-align: center;'>💬 Gemini AI Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat session
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro")
    st.session_state.chat_session = model.start_chat(history=[])

# Load existing chat history or initialize new one
if "messages" not in st.session_state:
    chat_history = load_chat_history()
    
    # If chat history is empty, add a greeting message
    if not chat_history:
        chat_history = [{"role": "assistant", "content": "Hello! 👋 I'm your AI assistant. How can I help you today?"}]
    
    st.session_state.messages = chat_history

# Display previous messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f"<div class='user-container'><div class='user-bubble'>{content}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-container'><div class='ai-bubble'>{content}</div></div>", unsafe_allow_html=True)

# User input field
prompt = st.chat_input("Ask me anything...")
if prompt:
    # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-container'><div class='user-bubble'>{prompt}</div></div>", unsafe_allow_html=True)

    # Get AI response
    response = st.session_state.chat_session.send_message(prompt)
    ai_reply = response.text

    # Add AI message to session history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.markdown(f"<div class='ai-container'><div class='ai-bubble'>{ai_reply}</div></div>", unsafe_allow_html=True)

    # Save updated chat history
    save_chat_history(st.session_state.messages)
