# 🗣️ Pronunciation Analysis System (English & Japanese)

An interactive, full-stack AI speech recognition, acoustic prosody analysis, and pronunciation scoring system supporting English and Japanese language learning.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-emerald.svg)
![Librosa](https://img.shields.io/badge/Librosa-1.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

---

## ✨ Key Features

- **Dual Language Support**: English (IPA, consonant clusters, minimal pairs) and Japanese (morae timing, pitch accent, long vowels, double consonants).
- **Acoustic & Prosody Analysis**:
  - Fundamental pitch frequency ($F_0$) tracking using `librosa.pyin`.
  - Pitch curve similarity matching via Dynamic Time Warping (DTW).
  - Energy RMS envelopes, speech duration, and acoustic clarity scoring.
- **Phonetic Distance & Alignment**:
  - Levenshtein dynamic programming alignment between target phonemes and spoken transcript.
  - Color-coded phoneme breakdown cards (*Match*, *Substitution*, *Omission*, *Extra Sound*).
- **Interactive Web Interface**:
  - Real-time audio recording using Web Audio API with frequency visualizer.
  - Native Text-to-Speech (TTS) reference audio playback.
  - Overlay chart comparing Target Pitch Curve vs. Spoken Pitch Curve.
  - Composite multi-metric score gauge & actionable coaching tips.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, FastAPI, Uvicorn, Librosa, NumPy, SciPy, SoundFile, SpeechRecognition
- **Frontend**: HTML5, Vanilla CSS (Glassmorphic Dark Mode), JavaScript (Web Audio API, HTML5 Canvas)

---

## 📁 Project Structure

```
├── app/
│   ├── main.py                     # FastAPI application & /api/analyze endpoints
│   ├── analyzer/
│   │   ├── acoustic_analyzer.py    # Librosa pitch tracking & energy envelope
│   │   ├── phonetic_analyzer.py    # Phoneme breakdown & Levenshtein alignment
│   │   └── speech_recognizer.py    # Speech transcription & audio conversion
│   └── data/
│       └── word_catalog.py         # English & Japanese practice catalog
├── static/
│   ├── index.html                  # Main dashboard layout
│   ├── css/style.css               # Styling & responsive design
│   └── js/
│       ├── app.js                  # Main controller logic
│       ├── audio_recorder.js       # Microphone recorder & frequency bars
│       └── visualizer.js           # Pitch contour canvas renderer
├── tests/
│   └── test_analyzer.py            # Unit test suite
├── run.py                          # Launcher script
└── requirements.txt                # Dependencies
```

---

## 🚀 Quick Start

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/balazoro08/Pronunciation-Analysis-System.git
   cd Pronunciation-Analysis-System
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 🧪 Running Tests

```bash
python -m pytest tests/test_analyzer.py -v
```

---

## 📜 License

MIT License © 2026
