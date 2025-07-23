# ChironX

A web-based agentic AI trainer that analyzes guitar technique from video, provides spoken feedback, tracks stats, and proactively coaches. Built for the Agentic AI Hackathon (July 25, 2025).

**Inspired by [farzaa/gemini-bball](https://github.com/farzaa/gemini-bball) for video-based skill analysis.**

## Features
- Multi-agent system (Vertex AI, Gemini, TTS, Firebase)
- Video upload & simulated live mode
- Audio (TTS) feedback + text logs
- Extensible "Skills Studio" (e.g., piano, drums)

## Tech Stack
- Backend: Python 3.12+ (Vertex AI, Gemini, TTS, Firebase)
- Frontend: HTML/JS (Firebase Hosting)
- Google Cloud: Vertex AI, Gemini, TTS, Firebase

## Setup
1. **Enable Google Cloud APIs:** Vertex AI, Gemini, TTS, Firebase (if using full features)
2. **Add API keys/config:**
   - In `backend/agents.py`, uncomment and fill in:
     ```python
     genai.configure(api_key='YOUR_API_KEY')
     aiplatform.init(project='YOUR_PROJECT_ID')
     db = firestore.Client()
     storage_client = storage.Client()
     ```
   - For MVP demo, Gemini and Firebase are mocked/skipped.
3. **Install backend dependencies:**
   ```bash
   pip install flask flask-cors google-cloud-aiplatform google-cloud-texttospeech google-cloud-firestore google-cloud-storage google-generativeai opencv-python numpy
   ```
4. **Run backend locally:**
   ```bash
   python backend/app.py
   ```
   - The backend will listen on `http://localhost:5001`.
5. **Run frontend:**
   - Open `frontend/index.html` directly in your browser (or deploy to Firebase Hosting for production).

## Usage
- Upload a guitar video (MP4) in the web UI.
- The backend analyzes the video, generates audio feedback, and returns logs and metrics.
- Audio feedback is played, logs are shown, and overlay displays detected chord/flaws/accuracy.
- Live mode is stubbed (MVP focus is upload flow).

## MVP Limitations
- Gemini and Firebase are mocked (no real AI/DB calls in MVP).
- TTS works locally; audio is served from backend.
- Live mode and Skills Studio navigation are placeholders.

## Demo Script (3-min Video)
1. **Intro:**
   - "This is ChironX, a web-based AI trainer for guitar technique."
2. **Upload Flow:**
   - "Let's upload a guitar video."
   - Show video upload, preview, and backend processing.
3. **Feedback:**
   - "The app analyzes your playing, gives spoken feedback, and shows stats and detected flaws."
   - Play audio feedback, show logs and overlay.
4. **Agentic Chain:**
   - "Multiple agents analyze, track stats, coach, and generate audio—all autonomously."
5. **Extensibility:**
   - "Skills Studio lets you navigate to other skills, like piano or drums—coming soon!"
6. **Outro:**
   - "Built for the Agentic AI Hackathon, inspired by farzaa/gemini-bball."

## Architecture Diagram
<!--
flowchart TD
    A[User Uploads Video/Live] --> B[Backend: Analyzer (Gemini)]
    B --> C[Statistician (Firebase)]
    C --> D[Coach (Gemini)]
    D --> E[Automator (TTS, Storage)]
    E --> F[Frontend: Audio + Logs + Overlay]
    D -.-> G[Skills Studio Navigation]
-->

## Credits
- Inspired by farzaa/gemini-bball for video-based skill analysis.
- Built by [Your Name] for Agentic AI Hackathon 2025.
