"""
FastAPI Server for Pronunciation Analysis System.
Serves web application, processes audio analysis requests, and handles TTS synthesis.
"""

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

from app.data.word_catalog import PRACTICE_WORDS, get_word_by_id, get_words_by_language
from app.analyzer.acoustic_analyzer import analyze_acoustic_features
from app.analyzer.phonetic_analyzer import analyze_phonetics
from app.analyzer.speech_recognizer import transcribe_audio

app = FastAPI(title="Pronunciation Analysis System", version="1.0.0")

# Mount static files directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve main frontend page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Pronunciation Analysis System API is running!</h1>"


@app.get("/api/catalog")
async def get_catalog(lang: Optional[str] = None):
    """Get practice word catalog."""
    if lang in ["en", "ja"]:
        return {"words": get_words_by_language(lang)}
    return {"words": PRACTICE_WORDS}


@app.post("/api/analyze")
async def analyze_pronunciation(
    audio: UploadFile = File(...),
    target_word: str = Form(...),
    language: str = Form("en"),
    word_id: Optional[str] = Form(None)
):
    """
    Main API endpoint: Receives audio recording and target word parameters,
    runs acoustic & phonetic pipelines, computes composite scores and generates feedback.
    """
    try:
        audio_bytes = await audio.read()
        if not audio_bytes or len(audio_bytes) < 100:
            raise HTTPException(status_code=400, detail="Invalid audio file recorded.")

        target_info = get_word_by_id(word_id) if word_id else None

        # 1. Speech Recognition
        transcription_result = transcribe_audio(audio_bytes, target_word=target_word, language=language)
        recognized_text = transcription_result["recognized_text"]

        # 2. Phonetic Analysis
        target_phoneme_list = target_info.get("phonemes") if target_info else None
        phonetic_result = analyze_phonetics(
            target_word=target_word,
            recognized_text=recognized_text if recognized_text else target_word,
            language=language,
            target_phoneme_list=target_phoneme_list
        )

        # 3. Acoustic Prosody & Pitch Analysis
        acoustic_result = analyze_acoustic_features(audio_bytes, target_info)

        # 4. Composite Score Calculation
        phonetic_score = phonetic_result["phonetic_score"]
        pitch_score = acoustic_result["pitch_score"]
        fluency_score = acoustic_result["fluency_score"]
        clarity_score = acoustic_result["clarity_score"]

        overall_score = round(
            (phonetic_score * 0.45) +
            (pitch_score * 0.25) +
            (fluency_score * 0.15) +
            (clarity_score * 0.15),
            1
        )

        # Grade calculation
        if overall_score >= 90:
            grade = "S"
            grade_label = "Mastery - Excellent Native-like Pronunciation!"
        elif overall_score >= 80:
            grade = "A"
            grade_label = "Great - Clear & High Accuracy!"
        elif overall_score >= 70:
            grade = "B"
            grade_label = "Good - Clear & Understandable"
        elif overall_score >= 55:
            grade = "C"
            grade_label = "Developing - Needs Practice on Key Sounds"
        else:
            grade = "D"
            grade_label = "Needs Focus - Practice Rhythm & Articulation"

        # 5. Generate Tailored Feedback & Coaching Tips
        feedback_list = []

        if target_info and "tip" in target_info:
            feedback_list.append(f"💡 Key Tip: {target_info['tip']}")

        if language == "ja":
            if pitch_score < 75:
                feedback_list.append("🎵 Pitch Accent: Pay attention to high/low pitch transitions. Japanese pitch changes word meaning (e.g. 雨 vs 飴).")
            if acoustic_result["duration_sec"] < 0.6 and "Long Vowels" in str(target_info):
                feedback_list.append("⏱️ Mora Duration: Stretch long vowels (長音) or pause at double consonants (っ) for 1 full mora beat.")
        else:  # English
            if phonetic_score < 80:
                feedback_list.append("🗣️ Phonetic Accuracy: Focus on articulating consonant endings and vowel quality distinctly.")
            if acoustic_result["duration_sec"] > 2.0:
                feedback_list.append("⚡ Pacing: Try speaking a little more naturally without lingering too long between syllables.")

        if clarity_score > 85:
            feedback_list.append("✨ Signal Quality: Strong, clear audio recording!")

        return JSONResponse(content={
            "success": True,
            "target_word": target_word,
            "recognized_text": recognized_text if recognized_text else target_word,
            "language": language,
            "overall_score": overall_score,
            "grade": grade,
            "grade_label": grade_label,
            "metrics": {
                "phonetic_score": phonetic_score,
                "pitch_score": pitch_score,
                "fluency_score": fluency_score,
                "clarity_score": clarity_score
            },
            "phonetic_breakdown": phonetic_result["alignment"],
            "acoustic": acoustic_result,
            "transcription": transcription_result,
            "feedback": feedback_list
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
