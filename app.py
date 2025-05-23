from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# All 20 supported languages
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali",
    "pa": "Punjabi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic"
}

# Setup OpenAI key from environment
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Transcribe audio using Whisper
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

# Translate using ChatGPT
def translate_text(text, target_lang):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate this to {target_lang}"},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route("/")
def home():
    return "YouDub is running!"

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

        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(filename="audio.mp4")

        # Step 1: Transcribe
        transcript = transcribe_audio(audio_path)

        # Step 2: Translate
        translated_text = translate_text(transcript, LANGUAGES[lang_code])

        return jsonify({
            "message": "Audio downloaded and translated",
            "language": LANGUAGES[lang_code],
            "transcript": transcript,
            "translation": translated_text,
            "file": audio_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

