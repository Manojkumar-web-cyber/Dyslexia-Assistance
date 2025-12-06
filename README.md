#  AI-Powered Dyslexia Reading Assistant

## Project Overview

An intelligent, web-based learning platform designed specifically to support dyslexic readers with **real-time pronunciation analysis, personalized feedback, and adaptive difficulty levels**. Built with modern AI/ML technologies for production deployment.

## Key Features

### 1. **Speech Analysis Module** (ASR)
- Real-time speech-to-text transcription using Google Speech Recognition API
- Pronunciation accuracy analysis compared to expected text
- Phonetic error detection (th, ch, sh, ph combinations)
- Fluency scoring based on word rhythm consistency
- Skipped word identification

### 2. **Attention Tracking Module** (Webcam-based)
- MediaPipe Face Mesh for eye-gaze tracking
- Real-time focus level calculation (0-100%)
- Engagement score monitoring
- Fatigue detection based on head position & blink rate
- Gaze direction analysis (left/right/forward)

### 3. **Difficulty Adaptation Engine** (ML-powered)
- Linear Regression model for reading difficulty prediction
- Auto-scales based on: reading pace, error frequency, engagement level
- Dynamic content simplification for beginner levels
- Real-time font size, spacing, and word complexity adjustments
- 4 difficulty tiers: Beginner → Elementary → Intermediate → Advanced

### 4. **Multisensory Support System**
- **Text-to-Speech (TTS)**: pyttsx3 for accessible audio
- **Visual Cues**: Color-coded words (vowel-heavy/consonant-heavy/balanced)
- **Pronunciation Hints**: Specific guidance for challenging phonemes
- **Syllable Breakdown**: Visual word segmentation for phonetic learning

### 5. **AI Mentor Persona**
- Emotionally intelligent personalized feedback
- 3 personality modes: Friendly, Teacher-like, Calm
- Trend analysis over session history
- Smart recommendations based on error patterns
- Session summaries with performance metrics

---

##  Architecture


---

##  Deployment & Running

### **Local Development**


### **Production (with Gunicorn WSGI server)**


**Access:** `https://your-codespace-url-5000.app.github.dev`

---

## 📊 Technology Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Backend Framework** | Flask + Gunicorn | Lightweight, production-ready WSGI server |
| **ASR** | Google Speech Recognition API | Free, accurate, no API keys |
| **Eye Tracking** | MediaPipe Face Mesh | Lightweight, no GPU required, real-time |
| **ML Adaptation** | scikit-learn LinearRegression | Interpretable, fast, online learning |
| **Text-to-Speech** | pyttsx3 | Open-source, offline, dyslexia-friendly |
| **Frontend** | HTML5 + Vanilla JS | No dependencies, fast, responsive |
| **Deployment** | GitHub Codespaces | Free, pre-configured, cloud-ready |

---

##  AI/ML Models Used

### **1. Speech Analysis**
- Algorithm: Sequence Matching (difflib)
- Calculates word-level pronunciation accuracy
- Detects phonetic error patterns

### **2. Attention Tracking**
- Algorithm: MediaPipe Face Mesh Landmarks
- Calculates focus level from head stability
- Derives engagement from: focus (50%) + gaze (30%) + blink (20%)

### **3. Difficulty Prediction**
- Model: Linear Regression
- Input Features: [reading_pace, error_frequency, engagement_level]
- Output: Difficulty score (0.0 - 1.0) mapped to 4 levels
- Online Learning: Retrains slightly on each prediction

### **4. Multisensory Support**
- Algorithm: Rule-based text analysis
- Extracts challenging phonemes (th, ch, sh, ph, gh)
- Generates color codes based on vowel-consonant ratio
- Provides evidence-based pronunciation tips

### **5. Mentor AI**
- Algorithm: Trend analysis + heuristics
- Analyzes performance patterns over session history
- Generates contextual, emotionally intelligent feedback
- Adapts recommendations based on accuracy and engagement trends

---

##  Performance Metrics

- **Pronunciation Accuracy**: Compared via word-level matching + SequenceMatcher
- **Fluency Score**: Consistency of word rhythm (0-100%)
- **Focus Level**: Head stability analysis (0-100%)
- **Engagement**: Weighted combination of focus, gaze, and blink (0-100%)
- **Session Summary**: Aggregated metrics + personalized insights

---

## 🎓 Use Cases

✅ **Dyslexic Students**: Real-time support during reading practice  
✅ **ESL Learners**: Pronunciation guidance for non-native speakers  
✅ **Speech Therapy**: Objective metrics for progress tracking  
✅ **Reading Intervention**: Adaptive difficulty for differentiated learning  

---

## 🔐 Privacy & Security

- ✅ **No data storage**: All processing is session-based
- ✅ **Microphone access**: Requested with browser permission
- ✅ **Webcam access**: User-controlled (can be disabled)
- ✅ **No external logging**: All data stays local

---

## 📋 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyze-speech` | POST | Transcribe & analyze pronunciation |
| `/api/track-attention` | POST | Analyze webcam frame for attention |
| `/api/get-support` | POST | Generate pronunciation hints & visual cues |
| `/api/adapt-difficulty` | POST | Predict optimal difficulty level |
| `/api/adapt-content` | POST | Simplify content based on difficulty |
| `/api/get-mentor-feedback` | POST | Generate personalized AI feedback |
| `/api/end-session` | POST | Generate session summary & reset |

---

## 🛠️ Installation

### **Requirements**
- Python 3.12+
- Modern browser (Chrome, Firefox, Safari)
- Microphone & Webcam
- Internet connection (for Google Speech API)

### **Setup**


---

##  Dependencies

See `backend/requirements.txt`:
- Flask 2.3.0 (Web framework)
- SpeechRecognition 3.10.0 (ASR)
- MediaPipe 0.10.21 (Face tracking)
- scikit-learn 1.3.0 (ML models)
- pyttsx3 2.90 (Text-to-speech)
- OpenCV 4.8.0.76 (Image processing)

---

##  Author

**Manoj Kumar**  
AI/ML Engineering Student | India  
GitHub: [@Manojkumar-web-cyber](https://github.com/Manojkumar-web-cyber)

---

## 📄 License

MIT License - Free for educational and commercial use

---

##  Contributing

Contributions welcome! Open an issue or PR for improvements.

---

## 📞 Support

For issues, questions, or feedback: [Create a GitHub Issue](https://github.com/your-username/Dyslexia-Assistance/issues)

---

**Last Updated:** December 6, 2025  
**Status:**  Production Ready

