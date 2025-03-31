# Gemini AI Chatbot

A Streamlit-based chatbot powered by Google's Gemini API that answers only specific domain queries. 
The chatbot maintains a conversation history and restricts responses to given topics.


Installation

1. Install Dependencies
		> pip install -r requirements.txt 
				or
		> pip install streamlit google-generativeai python-dotenv

2. Generate and Set Up API Key
To use the "Gemini API", you need to generate an API key:
- Visit [Google AI Studio](https://aistudio.google.com/).
- Sign in with your Google account.
- Navigate to the API Keys section.
- Generate a new API key and copy it.

3. Set up the API key:
1. Create a `.env` file in the project directory.
2. Add the following line: 
   GEMINI_API_KEY=your_api_key_here
  
4. Run the Application:
	> streamlit run chat.py


Example Usage
1. Open the Streamlit web app (usually at `http://localhost:8501`).
2. Type a medical-related question in the chat box.
3. Press Enter to get a response from the AI.
4. Chat history is saved and loaded on each session.


File Structure

📂 Chatbot
├── 📜 chat.py             # Main application script
├── 📜 .env               # Environment file for API key
├── 📜 chat_history.json  # Chat history storage
├── 📜 requirements.txt   # Dependencies
└── 📜 README.md          # Documentation


Configuration
- Google Gemini API: The chatbot fetches responses using Gemini AI. Ensure you have an active API key from Google.
- Chat History: The chatbot saves the chat history in `chat_history.json`.


