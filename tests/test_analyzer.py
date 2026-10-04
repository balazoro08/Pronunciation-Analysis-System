"""
Unit & Integration Tests for Pronunciation Analysis System
"""

import io
import pytest
import numpy as np
import soundfile as sf
from fastapi.testclient import TestClient

from app.main import app
from app.data.word_catalog import PRACTICE_WORDS, get_words_by_language, get_word_by_id
from app.analyzer.phonetic_analyzer import (
    text_to_phonemes_english,
    text_to_phonemes_japanese,
    levenshtein_align,
    analyze_phonetics
)
from app.analyzer.acoustic_analyzer import (
    extract_pitch_contour,
    generate_reference_pitch_contour,
    compute_pitch_similarity,
    analyze_acoustic_features
)
from app.analyzer.speech_recognizer import convert_bytes_to_wav, transcribe_audio

client = TestClient(app)


def generate_synthetic_audio_bytes(duration_sec=1.0, sr=16000, freq=220.0):
    """Generate synthetic PCM WAV audio bytes for testing."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    # Sine wave representing vowel sound
    audio_data = (0.5 * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sr, format='WAV', subtype='PCM_16')
    return buffer.getvalue()


# --- CATALOG TESTS ---
def test_word_catalog():
    assert len(PRACTICE_WORDS) > 0
    en_words = get_words_by_language("en")
    ja_words = get_words_by_language("ja")
    assert len(en_words) > 0
    assert len(ja_words) > 0
    assert get_word_by_id("en_pronunciation") is not None


# --- PHONETIC ANALYZER TESTS ---
def test_phonetic_english():
    p = text_to_phonemes_english("pronunciation")
    assert "P" in p and "R" in p
    align = analyze_phonetics("Pronunciation", "Pronunciation", "en")
    assert align["phonetic_score"] == 100.0


def test_phonetic_japanese():
    p = text_to_phonemes_japanese("ありがとう")
    assert "A" in p and "RI" in p
    align = analyze_phonetics("切手", "きって", "ja")
    assert align["phonetic_score"] >= 70.0


def test_levenshtein_alignment():
    res = levenshtein_align(["R", "AY", "T"], ["L", "AY", "T"])
    assert res["distance"] == 1
    assert len(res["alignment"]) == 3
    assert res["alignment"][0]["status"] == "minor_error"  # R vs L substitution


# --- ACOUSTIC ANALYZER TESTS ---
def test_acoustic_extraction():
    audio_bytes = generate_synthetic_audio_bytes(duration_sec=1.0, freq=220.0)
    res = analyze_acoustic_features(audio_bytes, {"pitch_pattern": "H-L"})
    assert res["duration_sec"] >= 0.8
    assert res["pitch_score"] > 0
    assert len(res["user_pitch_curve"]) > 0


def test_pitch_similarity():
    ref = generate_reference_pitch_contour("H-L", 50)
    assert len(ref) == 50
    score = compute_pitch_similarity(ref, ref)
    assert score > 90.0


# --- API ENDPOINT TESTS ---
def test_api_catalog_endpoint():
    response = client.get("/api/catalog?lang=en")
    assert response.status_code == 200
    data = response.json()
    assert "words" in data
    assert len(data["words"]) > 0


def test_api_analyze_endpoint():
    audio_bytes = generate_synthetic_audio_bytes(duration_sec=1.0)
    files = {"audio": ("test.wav", audio_bytes, "audio/wav")}
    data = {
        "target_word": "Pronunciation",
        "language": "en",
        "word_id": "en_pronunciation"
    }
    response = client.post("/api/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "overall_score" in res
    assert "grade" in res
    assert "metrics" in res
    assert "phonetic_breakdown" in res
    assert "acoustic" in res
