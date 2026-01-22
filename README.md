# ⚡ AI Interview Coach

A professional AI-powered interview practice application built with **Streamlit**, **LangChain**, and **Google Gemini**.

This application simulates a real-time technical interview, acting as an expert interviewer. It conducts voice-interactive interviews based on your resume and a specific job description, providing real-time feedback and a final evaluation.

## 🚀 Features

- **Customized Interviews:** tailored questions based on your specific **Resume** and the target **Job Description**.
- **Voice Interaction:**
  - **Speech-to-Text:** Speak your answers naturally using the microphone.
  - **Text-to-Speech:** The AI reads out questions using a realistic voice.
- **Real-time Transcript:** View the conversation history in a chat-like interface.
- **Video Interface:** Simulates a video call environment with camera toggles.
- **Evaluation:** Provides a detailed analysis of your performance after the interview concludes.
- **Secure:** Uses local environment variables for API keys.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Model:** Google Gemini (via `langchain-google-genai`)
- **Orchestration:** [LangChain](https://python.langchain.com/)
- **Audio Processing:**
  - `SpeechRecognition`: For transcribing user audio.
  - `pyttsx3`: For generating AI voice audio.
  - `streamlit-mic-recorder`: For capturing audio from the browser.
- **Database:** SQLite (via `database.py`)

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd infosys-project-main
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need `ffmpeg` installed on your system if you encounter audio processing issues, though the current implementation is optimized for WAV web standards.*

3.  **Environment Setup:**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## ▶️ Usage

1.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

2.  **Workflow:**
    - **Login/Signup:** Create an account or log in.
    - **Setup:** Upload your Resume (PDF/Text) and paste the Job Description. Select your target Role.
    - **Interview:**
        - The AI will greet you and ask the first question.
        - Click the **🎙️ microphone icon** to record your answer.
        - The AI will listen, think, and respond vocally.
    - **Results:** Click the **📞 End Call** button to finish. The AI will generate a performance report.

## 📂 Project Structure

```
├── app.py                # Main application entry point
├── database.py           # SQLite database handling
├── langchain_utils.py    # LangChain & Gemini integration logic
├── utils.py              # Audio processing (TTS & STT helper functions)
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (API Keys)
└── views/                # UI Components
    ├── auth.py           # Login/Signup pages
    ├── setup.py          # Job & Resume setup page
    ├── interview.py      # Main interview interface
    └── result.py         # Final evaluation page
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
