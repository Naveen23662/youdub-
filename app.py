from flask import Flask, request, jsonify, send_from_directory
import os
import asyncio
import edge_tts
import openai

# Load OpenAI key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Supported languages (20 total)
LANGUAGES = {
    "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
    "ml": "Malayalam", "gu": "Gujarati", "mr": "Marathi", "bn": "Bengali", "pa": "Punjabi",
    "fr": "French", "es": "Spanish", "de": "German", "it": "Italian", "pt": "Portuguese",
    "ru": "Russian", "ja": "Japanese", "ko": "Korean", "zh": "Chinese", "ar": "Arabic"
}

# Edge TTS voice map
VOICE_MAP = {
    "en": "en-US-GuyNeural", "hi": "hi-IN-MadhurNeural", "te": "te-IN-MohanNeural",
    "ta": "ta-IN-ValluvarNeural", "kn": "kn-IN-GaganNeural", "ml": "ml-IN-MidhunNeural",
    "gu": "gu-IN-NiranjanNeural", "mr": "mr-IN-ManoharNeural", "bn": "bn-IN-TanishNeural",
    "pa": "pa-IN-BaljeetNeural", "fr": "fr-FR-HenriNeural", "es": "es-ES-AlvaroNeural",
    "de": "de-DE-ConradNeural", "it": "it-IT-GianniNeural", "pt": "pt-PT-DuarteNeural",
    "ru": "ru-RU-DmitryNeural", "ja": "ja-JP-KeitaNeural", "ko": "ko-KR-InJoonNeural",
    "zh": "zh-CN-YunhaoNeural", "ar": "ar-EG-SherifNeural"
}

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

def translate_text(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following to {target_language}"},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]

async def generate_dubbed_audio(text, lang_code, output_file):
    voice = VOICE_MAP.get(lang_code, "en-US-GuyNeural")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.route("/")
def home():
    return "YouDub API is running!"

@app.route("/dub", methods=["POST"])
def dub_video():
    try:
        from pytube import YouTube

        url = request.json.get("url")
        lang_code = request.json.get("lang")

        if not url or not lang_code:
            return jsonify({"error": "Missing 'url' or 'lang'"}), 400
        if lang_code not in LANGUAGES:
            return jsonify({"error": f"Unsupported language '{lang_code}'"}), 400

        # Step 1: Download audio
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(filename="audio.mp4")

        # Step 2: Transcribe
        transcript = transcribe_audio(audio_path)

        # Step 3: Translate
        translated_text = translate_text(transcript, LANGUAGES[lang_code])

        # Step 4: Generate dubbed audio
        filename = f"dubbed_{lang_code}.mp3"
        static_path = os.path.join("static", filename)
        asyncio.run(generate_dubbed_audio(translated_text, lang_code, static_path))

        return jsonify({
            "message": "Dubbed successfully",
            "language": LANGUAGES[lang_code],
            "transcript": transcript,
            "translation": translated_text,
            "download_url": f"https://youdub.onrender.com/static/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

