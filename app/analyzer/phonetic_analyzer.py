"""
Phonetic Analysis Engine for English and Japanese.
Handles phoneme mapping, Levenshtein distance alignment, and phoneme-level diagnostic scoring.
"""

import re
from typing import List, Dict, Any

# Simple English ARPAbet/g2p dictionary mapping fallback
ENGLISH_PHONEME_MAP = {
    "PRONUNCIATION": ["P", "R", "AH", "N", "AH", "N", "S", "IY", "EY", "SH", "AH", "N"],
    "THINK": ["TH", "IH", "NG", "K"],
    "RIGHT": ["R", "AY", "T"],
    "LIGHT": ["L", "AY", "T"],
    "RHYTHM": ["R", "IH", "DH", "AH", "M"],
    "COMFORTABLE": ["K", "AH", "M", "F", "T", "AH", "B", "AH", "L"],
    "HELLO": ["HH", "AH", "L", "OW"],
    "WORLD": ["W", "ER", "L", "D"],
    "SPEECH": ["S", "P", "IY", "CH"],
    "ENGLISH": ["IH", "NG", "G", "L", "IH", "SH"],
    "JAPANESE": ["JH", "AE", "P", "AH", "N", "IY", "Z"],
}

# Hiragana to Kana/Morae decomposition map
HIRAGANA_ROMAJI_MAP = {
    'あ': 'A', 'い': 'I', 'う': 'U', 'え': 'E', 'お': 'O',
    'か': 'KA', 'き': 'KI', 'く': 'KU', 'け': 'KE', 'こ': 'KO',
    'さ': 'SA', 'し': 'SHI', 'す': 'SU', 'せ': 'SE', 'そ': 'SO',
    'た': 'TA', 'ち': 'CHI', 'つ': 'TSU', 'て': 'TE', 'と': 'TO',
    'な': 'NA', 'に': 'NI', 'ぬ': 'NU', 'ね': 'NE', 'の': 'NO',
    'は': 'HA', 'ひ': 'HI', 'ふ': 'FU', 'へ': 'HE', 'ほ': 'HO',
    'ま': 'MA', 'み': 'MI', 'む': 'MU', 'め': 'ME', 'も': 'MO',
    'や': 'YA', 'ゆ': 'YU', 'よ': 'YO',
    'ら': 'RA', 'り': 'RI', 'る': 'RU', 'れ': 'RE', 'ろ': 'RO',
    'わ': 'WA', 'を': 'WO', 'ん': 'N',
    'が': 'GA', 'ぎ': 'GI', 'ぐ': 'GU', 'げ': 'GE', 'ご': 'GO',
    'ざ': 'ZA', 'じ': 'JI', 'ず': 'ZU', 'ぜ': 'ZE', 'ぞ': 'ZO',
    'だ': 'DA', 'ぢ': 'JI', 'づ': 'ZU', 'で': 'DE', 'ど': 'DO',
    'ば': 'BA', 'び': 'BI', 'ぶ': 'BU', 'べ': 'BE', 'ぼ': 'BO',
    'ぱ': 'PA', 'ぴ': 'PI', 'ぷ': 'PU', 'ぺ': 'PE', 'ぽ': 'PO',
    'っ': 'Q', 'ー': 'LONG'
}

# Common Practice Kanji to Hiragana dictionary
KANJI_READING_MAP = {
    "雨": "あめ",
    "飴": "あめ",
    "切手": "きって",
    "お母さん": "おかあさん",
    "新幹線": "しんかんせん",
    "ありがとう": "ありがとう",
}


def text_to_phonemes_english(text: str) -> List[str]:
    """Convert English text into phoneme tokens (ARPAbet)."""
    words = re.findall(r'\b\w+\b', text.upper())
    phonemes = []
    for w in words:
        if w in ENGLISH_PHONEME_MAP:
            phonemes.extend(ENGLISH_PHONEME_MAP[w])
        else:
            # Heuristic letter-to-sound fallback
            for char in w:
                if char in "AEIOU":
                    phonemes.append("VOWEL_" + char)
                else:
                    phonemes.append(char)
    return phonemes if phonemes else ["UNKNOWN"]


def text_to_phonemes_japanese(text: str) -> List[str]:
    """Convert Japanese text (Kanji/Kana/Romaji) into morae phoneme tokens."""
    text = text.strip()
    
    # Check if text is Kanji present in map
    if text in KANJI_READING_MAP:
        text = KANJI_READING_MAP[text]
    else:
        # Extract hiragana reading from parentheses if present e.g. 雨 (あめ)
        match = re.search(r'[\(（]([\u3040-\u309F\u30A0-\u30FF]+)[\)）]', text)
        if match:
            text = match.group(1)

    phonemes = []
    for char in text:
        if char in HIRAGANA_ROMAJI_MAP:
            phonemes.append(HIRAGANA_ROMAJI_MAP[char])
        elif 'A' <= char.upper() <= 'Z':
            phonemes.append(char.upper())
        elif char in [" ", "　", "(", ")", "（", "）"]:
            continue
        else:
            phonemes.append(char)
    return phonemes if phonemes else ["UNKNOWN"]



def levenshtein_align(target: List[str], spoken: List[str]) -> Dict[str, Any]:
    """
    Perform Levenshtein distance dynamic programming alignment between target and spoken phonemes.
    Returns distance, accuracy percentage, and phoneme breakdown list.
    """
    m, n = len(target), len(spoken)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if target[i - 1] == spoken[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Deletion
                    dp[i][j - 1],      # Insertion
                    dp[i - 1][j - 1]   # Substitution
                )

    # Traceback alignment
    i, j = m, n
    alignment = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and target[i - 1] == spoken[j - 1]:
            alignment.append({
                "target_phoneme": target[i - 1],
                "spoken_phoneme": spoken[j - 1],
                "status": "correct",
                "score": 100,
                "label": "Match"
            })
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Substitution (minor or major error)
            t_p, s_p = target[i - 1], spoken[j - 1]
            # Check if closely related (e.g. R vs L, B vs V, TH vs S)
            is_similar = (
                (t_p in ["R", "L"] and s_p in ["R", "L"]) or
                (t_p in ["TH", "DH", "S", "Z"] and s_p in ["TH", "DH", "S", "Z"]) or
                (t_p in ["B", "V", "F"] and s_p in ["B", "V", "F"]) or
                (t_p.startswith("VOWEL") and s_p.startswith("VOWEL"))
            )
            score = 65 if is_similar else 30
            status = "minor_error" if is_similar else "mispronounced"

            alignment.append({
                "target_phoneme": t_p,
                "spoken_phoneme": s_p,
                "status": status,
                "score": score,
                "label": f"Substituted ('{s_p}')"
            })
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j] == dp[i - 1][j] + 1):
            # Deletion (omitted target sound)
            alignment.append({
                "target_phoneme": target[i - 1],
                "spoken_phoneme": "-",
                "status": "mispronounced",
                "score": 0,
                "label": "Omitted"
            })
            i -= 1
        else:
            # Insertion (extra sound spoken)
            alignment.append({
                "target_phoneme": "-",
                "spoken_phoneme": spoken[j - 1],
                "status": "minor_error",
                "score": 40,
                "label": "Extra Sound"
            })
            j -= 1

    alignment.reverse()
    distance = dp[m][n]
    max_len = max(m, 1)

    # Calculate overall phonetic score
    raw_score = max(0.0, 100.0 - (distance / max_len) * 100.0)
    
    return {
        "distance": distance,
        "phonetic_score": round(raw_score, 1),
        "alignment": alignment,
        "target_phonemes": target,
        "spoken_phonemes": spoken
    }


def analyze_phonetics(target_word: str, recognized_text: str, language: str = "en", target_phoneme_list: List[str] = None) -> Dict[str, Any]:
    """
    Main entry point for phonetic comparison.
    Converts target & spoken texts to phonemes and computes alignment.
    """
    if target_phoneme_list and len(target_phoneme_list) > 0:
        target_p = target_phoneme_list
    else:
        if language == "ja":
            target_p = text_to_phonemes_japanese(target_word)
        else:
            target_p = text_to_phonemes_english(target_word)

    if language == "ja":
        spoken_p = text_to_phonemes_japanese(recognized_text)
    else:
        spoken_p = text_to_phonemes_english(recognized_text)

    # Edge case: if spoken recognized text is empty or unknown
    if not recognized_text or recognized_text.strip() == "":
        return {
            "phonetic_score": 0.0,
            "distance": len(target_p),
            "target_phonemes": target_p,
            "spoken_phonemes": [],
            "alignment": [
                {
                    "target_phoneme": p,
                    "spoken_phoneme": "-",
                    "status": "mispronounced",
                    "score": 0,
                    "label": "Not detected"
                } for p in target_p
            ]
        }

    # If exact string match
    if target_word.strip().lower() == recognized_text.strip().lower():
        return {
            "phonetic_score": 100.0,
            "distance": 0,
            "target_phonemes": target_p,
            "spoken_phonemes": target_p,
            "alignment": [
                {
                    "target_phoneme": p,
                    "spoken_phoneme": p,
                    "status": "correct",
                    "score": 100,
                    "label": "Perfect Match"
                } for p in target_p
            ]
        }

    return levenshtein_align(target_p, spoken_p)
