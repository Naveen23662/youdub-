from flask import Flask, request, render_template, send_file
import os
from pytube import YouTube
import whisper
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
from uuid import uuid4

app = Flask(__name__)
model = whisper.load_model("base")

LANGUAGES = {
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Urdu": "ur",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Russian": "ru"
}

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/download_and_dub', methods=['POST'])
def download_and_dub():
    url = request.form['url']
    target_lang = request.form['language']
    lang_code = LANGUAGES.get(target_lang)

    # 1. Download YouTube Audio
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    input_file = f"input_{uuid4().hex}.mp4"
    audio_stream.download(filename=input_file)

    # 2. Transcribe Audio
    result = model.transcribe(input_file)
    original_text = result['text']

    # 3. Translate Text
    translated_text = GoogleTranslator(source='auto', target=lang_code).translate(original_text)

    # 4. Generate Audio using Edge TTS
    output_file = f"dubbed_{uuid4().hex}.mp3"

    async def synthesize(text, file_path):
        tts = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural")  # You can choose voice based on lang_code
        await tts.save(file_path)

    asyncio.run(synthesize(translated_text, output_file))

    # 5. Serve dubbed audio file
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

