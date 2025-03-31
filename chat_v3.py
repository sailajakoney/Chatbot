import streamlit as st
import google.generativeai as genai
import os
import json
import fitz  # PyMuPDF for PDFs
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Document file (must be in the same directory)
DOCUMENT_PATH = "=machine_learning_intro.pdf"  # Change to your document name
CHAT_HISTORY_FILE = "chat_history.json"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# Load document text
if os.path.exists(DOCUMENT_PATH):
    document_text = extract_text_from_pdf(DOCUMENT_PATH)
else:
    document_text = "Document not found. Please upload a valid document."

# Initialize chat session
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro")  
    st.session_state.chat_session = model.start_chat(history=[])

# Function to chat with Gemini using only document text
def ask_gemini(query):
    """Send extracted text as context to Gemini API, restricting answers to the document."""
    response = st.session_state.chat_session.send_message([document_text[:5000], query])
    return response.text

# Function to load chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat history
def save_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(messages, file, indent=4)

# Custom CSS for chat UI
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
    st.write("1. Ask a  question.")
    st.write("2. Responses are based **only on the uploaded document**.")
    st.write("3. Chat history is saved.")

# Chat UI Title
st.markdown("<h1 style='text-align: center;'>💬 Document based AI Chatbot</h1>", unsafe_allow_html=True)

# Load chat history
if "messages" not in st.session_state:
    chat_history = load_chat_history()
    if not chat_history:
        chat_history = [{"role": "assistant", "content": "Hello! 👋 I'm your  AI assistant. Ask me anything from the document."}]
    st.session_state.messages = chat_history

# Display previous messages
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    css_class = "user-bubble" if role == "user" else "ai-bubble"
    container_class = "user-container" if role == "user" else "ai-container"
    st.markdown(f"<div class='{container_class}'><div class='{css_class}'>{content}</div></div>", unsafe_allow_html=True)

# User Input
prompt = st.chat_input("Ask a question based on the document...")
if prompt:
    # Store user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-container'><div class='user-bubble'>{prompt}</div></div>", unsafe_allow_html=True)

    # Get AI response (restricted to document)
    ai_reply = ask_gemini(prompt)

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.markdown(f"<div class='ai-container'><div class='ai-bubble'>{ai_reply}</div></div>", unsafe_allow_html=True)

    # Save updated chat history
    save_chat_history(st.session_state.messages)
