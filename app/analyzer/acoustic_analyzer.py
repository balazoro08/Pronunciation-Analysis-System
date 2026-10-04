"""
Acoustic Processing & Prosody Analysis Engine using Librosa & NumPy.
Extracts Pitch (F0), Energy RMS, Duration, MFCCs, and computes acoustic similarity.
"""

import io
import numpy as np
import librosa
import soundfile as sf
from typing import Dict, Any, Tuple, List


def load_audio_bytes(audio_bytes: bytes) -> Tuple[np.ndarray, int]:
    """
    Load raw audio bytes (WAV, OGG, WEBM, FLAC) into float32 array y and sample rate sr.
    """
    buffer = io.BytesIO(audio_bytes)
    try:
        y, sr = sf.read(buffer, dtype='float32')
        if len(y.shape) > 1:
            y = np.mean(y, axis=1)  # convert stereo to mono
        # Resample to standard 16kHz for speech analysis
        if sr != 16000:
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            sr = 16000
    except Exception as e:
        # Fallback to librosa.load
        buffer.seek(0)
        y, sr = librosa.load(buffer, sr=16000, mono=True)

    # Trim leading/trailing silence
    y_trimmed, _ = librosa.effects.trim(y, top_db=25)
    if len(y_trimmed) > 0:
        y = y_trimmed

    # Normalize amplitude
    max_val = np.max(np.abs(y))
    if max_val > 0:
        y = y / max_val

    return y, sr


def extract_pitch_contour(y: np.ndarray, sr: int = 16000) -> Tuple[List[float], float, float]:
    """
    Extract fundamental pitch frequency F0 curve using pYIN algorithm.
    Returns (pitch_curve_hz, mean_f0, std_f0).
    """
    if len(y) < 512:
        return [0.0], 0.0, 0.0

    # Human voice F0 range: 65 Hz to 450 Hz
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),  # ~65 Hz
        fmax=librosa.note_to_hz('C6'),  # ~1046 Hz
        sr=sr,
        frame_length=1024,
        hop_length=256
    )

    # Replace NaNs with 0.0 for unvoiced segments
    f0_clean = np.nan_to_num(f0, nan=0.0)
    voiced_f0 = f0_clean[f0_clean > 0]

    mean_f0 = float(np.mean(voiced_f0)) if len(voiced_f0) > 0 else 0.0
    std_f0 = float(np.std(voiced_f0)) if len(voiced_f0) > 0 else 0.0

    # Downsample pitch curve to ~30-50 points for visual canvas graph rendering
    points = min(50, len(f0_clean))
    if len(f0_clean) > points:
        indices = np.linspace(0, len(f0_clean) - 1, points, dtype=int)
        pitch_curve = [round(float(f0_clean[idx]), 1) for idx in indices]
    else:
        pitch_curve = [round(float(val), 1) for val in f0_clean]

    return pitch_curve, round(mean_f0, 1), round(std_f0, 1)


def extract_energy_envelope(y: np.ndarray, frame_length: int = 1024, hop_length: int = 256) -> List[float]:
    """Calculate Root Mean Square (RMS) energy envelope over time."""
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    # Downsample to 50 points
    points = min(50, len(rms))
    if len(rms) > points:
        indices = np.linspace(0, len(rms) - 1, points, dtype=int)
        energy_curve = [round(float(rms[idx]), 3) for idx in indices]
    else:
        energy_curve = [round(float(val), 3) for val in rms]
    return energy_curve


def generate_reference_pitch_contour(expected_pattern: str = "H-L", num_points: int = 50) -> List[float]:
    """Generate a synthetic native reference pitch curve (Hz) based on pattern."""
    x = np.linspace(0, 1, num_points)
    base_f0 = 180.0  # nominal pitch

    if "H-L" in expected_pattern or "Atamadaka" in expected_pattern:
        # Starts High, drops Low
        curve = base_f0 + 50 * np.cos(x * np.pi * 0.8)
    elif "L-H" in expected_pattern or "Heiban" in expected_pattern:
        # Starts Low, rises High
        curve = base_f0 + 45 * np.sin(x * np.pi * 0.8)
    elif "L-H-L" in expected_pattern:
        # Low -> High -> Low bell curve
        curve = base_f0 + 60 * np.sin(x * np.pi)
    else:
        # Gentle curve for normal polysyllabic words
        curve = base_f0 + 35 * np.sin(x * np.pi * 1.5)

    return [round(float(v), 1) for v in curve]


def compute_pitch_similarity(user_pitch: List[float], ref_pitch: List[float]) -> float:
    """
    Compute pitch contour similarity score (0 - 100%) using dynamic time warping / correlation.
    """
    u_valid = [p for p in user_pitch if p > 0]
    if not u_valid:
        return 40.0

    # Normalize pitch contours to relative zero-mean unit-variance
    u_norm = (np.array(user_pitch) - np.mean(u_valid)) / (np.std(u_valid) + 1e-5)
    r_norm = (np.array(ref_pitch) - np.mean(ref_pitch)) / (np.std(ref_pitch) + 1e-5)

    # Resample to match lengths
    target_len = min(len(u_norm), len(r_norm))
    if target_len < 5:
        return 50.0

    u_res = np.interp(np.linspace(0, 1, 50), np.linspace(0, 1, len(u_norm)), u_norm)
    r_res = np.interp(np.linspace(0, 1, 50), np.linspace(0, 1, len(r_norm)), r_norm)

    # Correlation coefficient
    corr = np.corrcoef(u_res, r_res)[0, 1]
    if np.isnan(corr):
        corr = 0.5

    # Map correlation [-1, 1] to score [30, 100]
    score = 65.0 + (corr * 35.0)
    return round(float(np.clip(score, 10.0, 100.0)), 1)


def analyze_acoustic_features(audio_bytes: bytes, target_word_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main entry point for acoustic audio analysis.
    Loads audio, extracts pitch, energy, duration, and compares against target metrics.
    """
    y, sr = load_audio_bytes(audio_bytes)
    duration_sec = len(y) / float(sr)

    pitch_curve, mean_f0, std_f0 = extract_pitch_contour(y, sr)
    energy_curve = extract_energy_envelope(y)

    pattern = target_word_info.get("pitch_pattern", "H-L") if target_word_info else "H-L"
    ref_pitch_curve = generate_reference_pitch_contour(pattern, len(pitch_curve))

    pitch_score = compute_pitch_similarity(pitch_curve, ref_pitch_curve)

    # Evaluate Fluency & Tempo
    # Normal word utterance duration is typically 0.4s to 2.2s
    if 0.5 <= duration_sec <= 2.2:
        fluency_score = 90.0 + (10.0 * (1.0 - abs(duration_sec - 1.2) / 1.2))
    elif duration_sec < 0.4:
        fluency_score = 55.0  # Too fast / truncated
    else:
        fluency_score = 65.0  # Prolonged / hesitations

    fluency_score = round(float(np.clip(fluency_score, 20.0, 100.0)), 1)

    # Signal Clarity Score based on energy & SNR estimate
    mean_energy = np.mean(energy_curve) if len(energy_curve) > 0 else 0.0
    clarity_score = round(float(np.clip(70.0 + (mean_energy * 100.0), 40.0, 98.0)), 1)

    return {
        "duration_sec": round(duration_sec, 2),
        "mean_f0_hz": mean_f0,
        "std_f0_hz": std_f0,
        "user_pitch_curve": pitch_curve,
        "ref_pitch_curve": ref_pitch_curve,
        "energy_curve": energy_curve,
        "pitch_score": pitch_score,
        "fluency_score": fluency_score,
        "clarity_score": clarity_score
    }
