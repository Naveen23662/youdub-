import edge_tts

# Gender-neutral fallback mapping
VOICE_MAP = {
    "english": "en-IN-PrabhatNeural",
    "hindi": "hi-IN-MadhurNeural",
    "telugu": "te-IN-MohanNeural",
    "tamil": "ta-IN-ValluvarNeural",
    "kannada": "kn-IN-GaganNeural",
    "malayalam": "ml-IN-MidhunNeural",
    "bengali": "bn-IN-TanishNeural",
    "marathi": "mr-IN-AaravNeural",
    "gujarati": "gu-IN-NiranjanNeural",
    "punjabi": "pa-IN-SomarNeural",
    "french": "fr-FR-HenriNeural",
    "german": "de-DE-ConradNeural",
    "spanish": "es-ES-AlvaroNeural",
    "japanese": "ja-JP-KeitaNeural",
    "korean": "ko-KR-InJoonNeural",
    "russian": "ru-RU-DmitryNeural",
    "italian": "it-IT-BenignoNeural",
    "arabic": "ar-EG-SherifNeural",
    "portuguese": "pt-PT-DuarteNeural",
    "indonesian": "id-ID-ArdiNeural"
}

def generate_edge_audio(text, output_path, language):
    voice = VOICE_MAP.get(language.lower(), "en-IN-PrabhatNeural")
    communicate = edge_tts.Communicate(text, voice)
    with open(output_path, "wb") as f:
        for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

