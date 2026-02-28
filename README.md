# ⚡ Coach.AI - Pro Interview Coach

A professional AI-powered interview practice application built with **Streamlit**, **LangChain**, and **Google Gemini**.

This application simulates a real-time technical interview, acting as an expert interviewer. It evaluates your resume against a specific job description, conducts a voice-interactive interview, and provides detailed graphical feedback, ATS scoring, and historical tracking.

## 🚀 Key Features

- **Dynamic Theming:** Seamlessly toggle between a beautifully designed Light and Dark mode UI with custom CSS glassmorphism components.
- **ATS Resume Evaluation:** 
  - Get an instant "Applicant Tracking System" match score before your interview.
  - See detailed breakdown rings and specific keyword recommendations tailored to the Job Description.
- **Customized AI Interviews:** 
  - Tailored questions based on your specific **Resume** and the target **Job Description**.
- **Voice Interaction:**
  - **Speech-to-Text:** Speak your answers naturally using the microphone.
  - **Text-to-Speech:** The AI reads out questions using a realistic voice.
- **Dashboard Results:**
  - View a highly detailed, graphical dashboard summarizing your recent performance.
  - Includes progress charts, percentage breakdowns for Speech/Content/Emotions, and actionable AI feedback.
- **Interview History System:**
  - All past interviews are automatically saved to a local SQLite database.
  - Revisit the "History" tab anytime to review specific dates, scores, and complete word-for-word transcripts of your past sessions.
- **Advanced Resume Parsing:** 
  - Extracts text from PDF documents and relies on OCR for Image-based resumes.
- **Secure:** Uses local environment variables for API keys and local databases for user data.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) with heavy Custom HTML/CSS/JS injections
- **AI Model:** Google Gemini (via `langchain-google-genai`)
- **Orchestration:** [LangChain](https://python.langchain.com/)
- **Text Processing:**
  - `langchain-text-splitters`, `pytesseract`, `Pillow`, `pypdf`
- **Audio Processing:**
  - `SpeechRecognition`, `pyttsx3`, `streamlit-mic-recorder`
- **Database:** SQLite (Local History & Auth Storage)

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd coach.ai
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need `ffmpeg` installed on your system if you encounter audio processing issues. You also need Tesseract installed for OCR features.*

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
    - **Login/Signup:** Create a secure local account.
    - **Setup:** Upload your Resume (PDF/Text) and paste the Job Description. Select your target Role.
    - **ATS Check:** Review your resume's match score against the job description.
    - **Interview:**
        - Click the **🎙️ microphone icon** to record your answers to the AI.
        - Toggle your camera or view the live transcript.
    - **Results & History:** Click **End Call** to view your dashboard breakdown, or visit the **History** tab to see your past growth.

## 📂 Project Structure

```
├── app.py                # Main application & routing
├── database.py           # SQLite user and history storage
├── langchain_utils.py    # LangChain & Gemini AI logic
├── styles.py             # Global CSS and JS Theme Toggles
├── utils.py              # Audio/TTS/STT and local TTS scoring helpers
├── views/                # UI Components
    ├── auth.py           # Login/Signup logic
    ├── setup.py          # Job & Resume upload
    ├── ats_score.py      # Pre-interview resume grading UI
    ├── interview.py      # Main interactive A/V interface
    ├── result.py         # Graphical dashboard and charts
    └── history.py        # Database lookup and transcript review
```
