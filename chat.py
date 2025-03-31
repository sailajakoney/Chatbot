import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load API key from .env file
load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load API key from Streamlit Secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set Streamlit UI configuration
st.set_page_config(page_title="Gemini AI Chatbot", layout="wide")

# System instruction to restrict chatbot responses
SYSTEM_INSTRUCTION = "You are an AI that only answers questions related to medical topics. Do not answer questions outside this domain."

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

# Sidebar Instructions
with st.sidebar:
    st.title("🛠 How to Use")
    st.write("1. Type a **medical-related** question in the chat box.")
    st.write("2. Press **Enter** to send.")
    st.write("3. If your question is not related to medical topics, it will be rejected.")
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
        chat_history = [{"role": "assistant", "content": "Hello! 👋 I'm a medical AI assistant. Ask me about health, diseases, and treatments!"}]
    
    st.session_state.messages = chat_history

# Display previous messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f"<div class='user-container'><div class='user-bubble'>{content}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-container'><div class='ai-bubble'>{content}</div></div>", unsafe_allow_html=True)

# User input
prompt = st.chat_input("Ask me a medical question...")
if prompt:
    # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-container'><div class='user-bubble'>{prompt}</div></div>", unsafe_allow_html=True)

    # Get AI response with system instruction
    response = st.session_state.chat_session.send_message([SYSTEM_INSTRUCTION, prompt])
    ai_reply = response.text

    # Ensure AI remains responsive
    if "sorry" in ai_reply.lower() or "cannot" in ai_reply.lower():
        ai_reply += " Feel free to ask another medical-related question!"
    
    # Add AI response to session history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.markdown(f"<div class='ai-container'><div class='ai-bubble'>{ai_reply}</div></div>", unsafe_allow_html=True)

    # Save updated chat history
    save_chat_history(st.session_state.messages)
