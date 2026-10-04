"""
Word Catalog for English and Japanese Pronunciation Practice.
Contains target words, phoneme sequences, IPA/Kana representations, pitch contours, and tips.
"""

PRACTICE_WORDS = [
    # --- ENGLISH WORDS ---
    {
        "id": "en_pronunciation",
        "word": "Pronunciation",
        "language": "en",
        "category": "Polysyllabic & Stress",
        "difficulty": "Intermediate",
        "ipa": "prəˌnʌn.siˈeɪ.ʃən",
        "phonemes": ["P", "R", "AH", "N", "AH", "N", "S", "IY", "EY", "SH", "AH", "N"],
        "display_phonemes": ["prə", "nʌn", "si", "eɪ", "ʃən"],
        "pitch_profile": "L-L-H-L",
        "tip": "Primary stress is on 'eɪ' (pro-NUN-ci-A-tion). Ensure clear separation between NUN and CI.",
        "translation": "発音 (Hatsuon)"
    },
    {
        "id": "en_th_think",
        "word": "Think",
        "language": "en",
        "category": "Minimal Pair / TH Sound",
        "difficulty": "Beginner",
        "ipa": "θɪŋk",
        "phonemes": ["TH", "IH", "NG", "K"],
        "display_phonemes": ["θ", "ɪ", "ŋk"],
        "pitch_profile": "H-L",
        "tip": "Place the tip of your tongue between your top and bottom teeth for the 'th' (θ) sound without voicing.",
        "translation": "考える (Kangaeru)"
    },
    {
        "id": "en_rl_right",
        "word": "Right",
        "language": "en",
        "category": "R vs L Distinction",
        "difficulty": "Beginner",
        "ipa": "raɪt",
        "phonemes": ["R", "AY", "T"],
        "display_phonemes": ["r", "aɪ", "t"],
        "pitch_profile": "H-L",
        "tip": "Curl your tongue slightly back without touching the roof of your mouth for the American 'R'.",
        "translation": "正しい / 右 (Tadashii / Migi)"
    },
    {
        "id": "en_rl_light",
        "word": "Light",
        "language": "en",
        "category": "R vs L Distinction",
        "difficulty": "Beginner",
        "ipa": "laɪt",
        "phonemes": ["L", "AY", "T"],
        "display_phonemes": ["l", "aɪ", "t"],
        "pitch_profile": "H-L",
        "tip": "Touch the tip of your tongue firmly against the alveolar ridge (behind top front teeth) for 'L'.",
        "translation": "光 / 軽い (Hikari / Karui)"
    },
    {
        "id": "en_rhythm",
        "word": "Rhythm",
        "language": "en",
        "category": "Consonant Clusters",
        "difficulty": "Advanced",
        "ipa": "ˈrɪð.əm",
        "phonemes": ["R", "IH", "DH", "AH", "M"],
        "display_phonemes": ["rɪ", "ðəm"],
        "pitch_profile": "H-L",
        "tip": "Transition smoothly from voiced 'TH' (ð) directly to syllabic 'M' without adding an extra vowel.",
        "translation": "リズム (Rizumu)"
    },
    {
        "id": "en_comfortable",
        "word": "Comfortable",
        "language": "en",
        "category": "Vowels & Reduction",
        "difficulty": "Advanced",
        "ipa": "ˈkʌmf.tə.bəl",
        "phonemes": ["K", "AH", "M", "F", "T", "AH", "B", "AH", "L"],
        "display_phonemes": ["kʌmf", "tə", "bəl"],
        "pitch_profile": "H-L-L",
        "tip": "Native speakers often reduce this to 3 syllables: 'KUMF-ter-bul'. Drop the second 'o'.",
        "translation": "快適な (Kaiteki na)"
    },

    # --- JAPANESE WORDS ---
    {
        "id": "ja_arigatou",
        "word": "ありがとう",
        "language": "ja",
        "category": "Daily Phrases & Long Vowels",
        "difficulty": "Beginner",
        "ipa": "aɾiɡatoː",
        "romaji": "arigatou",
        "phonemes": ["A", "RI", "GA", "TO", "U"],
        "display_phonemes": ["あ", "り", "が", "と", "う"],
        "morae": ["a", "ri", "ga", "to", "o"],
        "pitch_pattern": "L-H-H-H-L (Heiban pitch)",
        "tip": "Hold the 'tou' (とー) sound for 2 morae. Keep pitch smooth across 'ri-ga-to'.",
        "translation": "Thank you"
    },
    {
        "id": "ja_ame_rain",
        "word": "雨 (あめ)",
        "language": "ja",
        "category": "Pitch Accent Distinction",
        "difficulty": "Intermediate",
        "ipa": "ame",
        "romaji": "ame",
        "phonemes": ["A", "ME"],
        "display_phonemes": ["あ", "め"],
        "morae": ["a", "me"],
        "pitch_pattern": "H-L (Atamadaka pitch: HIGH-low)",
        "tip": "High pitch on 'A', drops down sharply on 'ME'. Contrast with 飴 (Candy: L-H).",
        "translation": "Rain (雨)"
    },
    {
        "id": "ja_ame_candy",
        "word": "飴 (あめ)",
        "language": "ja",
        "category": "Pitch Accent Distinction",
        "difficulty": "Intermediate",
        "ipa": "ame",
        "romaji": "ame",
        "phonemes": ["A", "ME"],
        "display_phonemes": ["あ", "め"],
        "morae": ["a", "me"],
        "pitch_pattern": "L-H (Heiban pitch: low-HIGH)",
        "tip": "Start lower on 'A' and rise to high pitch on 'ME'.",
        "translation": "Candy (飴)"
    },
    {
        "id": "ja_kitte",
        "word": "切手 (きって)",
        "language": "ja",
        "category": "Sokutei (Small Tsu / Geminate)",
        "difficulty": "Intermediate",
        "ipa": "kitːe",
        "romaji": "kitte",
        "phonemes": ["KI", "Q", "TE"],
        "display_phonemes": ["き", "っ", "て"],
        "morae": ["ki", "Q", "te"],
        "pitch_pattern": "L-H-L",
        "tip": "Pause your breath briefly for 1 full mora beat at 'っ' before pronouncing 'て'.",
        "translation": "Postage Stamp"
    },
    {
        "id": "ja_okaasan",
        "word": "お母さん (おかあさん)",
        "language": "ja",
        "category": "Long Vowels (Chōon)",
        "difficulty": "Beginner",
        "ipa": "okaːsaɴ",
        "romaji": "okaasan",
        "phonemes": ["O", "KA", "A", "SA", "N"],
        "display_phonemes": ["お", "か", "あ", "さ", "ん"],
        "morae": ["o", "ka", "a", "sa", "n"],
        "pitch_pattern": "L-H-H-H-L",
        "tip": "Ensure 'かあ' is held for two distinct beats. Don't rush into 'さん'.",
        "translation": "Mother"
    },
    {
        "id": "ja_shinkansen",
        "word": "新幹線 (しんかんせん)",
        "language": "ja",
        "category": "Nasal 'N' (Hatsuon) & Rhythm",
        "difficulty": "Advanced",
        "ipa": "ɕiɴkaɴseɴ",
        "romaji": "shinkansen",
        "phonemes": ["SHI", "N", "KA", "N", "SE", "N"],
        "display_phonemes": ["し", "ん", "か", "ん", "せ", "ん"],
        "morae": ["shi", "n", "ka", "n", "se", "n"],
        "pitch_pattern": "L-H-H-H-H-L",
        "tip": "Total 6 morae. Each 'ん' takes equal time beat as 'し' or 'か'. Maintain steady metronome pace.",
        "translation": "Bullet Train"
    }
]

def get_word_by_id(word_id: str):
    """Find word configuration by ID."""
    for item in PRACTICE_WORDS:
        if item["id"] == word_id:
            return item
    return None

def get_words_by_language(lang: str):
    """Filter catalog by language ('en' or 'ja')."""
    return [item for item in PRACTICE_WORDS if item["language"] == lang]
