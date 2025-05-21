from flask import Flask, render_template, request, send_file
from deep_translator import GoogleTranslator
import os
import yt_dlp
import edge_tts
import uuid
import asyncio

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Dubbing endpoint
@app.route('/download_and_dub', methods=['POST'])
def download_and_dub():
    url = request.form['url']
    target_lang = request.form['language']

    # Step 1: Download audio
    audio_id = str(uuid.uuid4())
    input_audio = f"static/input_{audio_id}.mp3"
    output_audio = f"static/output_{audio_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': input_audio,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Download error: {str(e)}"

    # Step 2: Transcribe
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        with open(input_audio, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
        original_text = transcript["text"]
    except Exception as e:
        return f"Transcription failed: {str(e)}"

    # Step 3: Translate
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
    except Exception as e:
        return f"Translation error: {str(e)}"

    # Step 4: Text to speech
    async def generate():
        communicate = edge_tts.Communicate(translated_text, f"{target_lang}-IN-NeerjaNeural")
        await communicate.save(output_audio)

    try:
        asyncio.run(generate())
    except Exception as e:
        return f"TTS failed: {str(e)}"

    return render_template('result.html', audio_file=output_audio)

# Audio file route
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_file(f'static/{filename}')

