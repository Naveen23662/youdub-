from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Supported languages dictionary (you can expand this list)
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

@app.route("/")
def home():
    return "YouDub is running!"

@app.route("/dub", methods=["POST"])
def dub_video():
    try:
        # ✅ Import inside route to save memory
        from pytube import YouTube

        # ✅ Get URL and language from request
        url = request.json.get("url")
        lang_code = request.json.get("lang")

        if not url or not lang_code:
            return jsonify({"error": "Missing 'url' or 'lang'"}), 400

        if lang_code not in LANGUAGES:
            return jsonify({"error": f"Unsupported language '{lang_code}'"}), 400

        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(filename="audio.mp4")

        # ✅ Placeholder - you can add translation/dubbing here
        return jsonify({
            "message": "Audio downloaded successfully",
            "language": LANGUAGES[lang_code],
            "file": audio_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

