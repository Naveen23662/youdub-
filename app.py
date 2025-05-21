from flask import Flask, render_template, request, send_file
import os
from deep_translator import GoogleTranslator
from gtts import gTTS
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_and_dub', methods=['POST'])
def download_and_dub():
    url = request.form['url']
    lang_code = request.form['language']

    # Step 1: Download YouTube audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'static/input.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'audio')

    input_path = 'static/input.mp3'

    # Step 2: Transcribe - mock for now
    english_text = "This is a sample sentence from the video."

    # Step 3: Translate
    translated = GoogleTranslator(source='auto', target=lang_code).translate(english_text)

    # Step 4: Dub using gTTS
    tts = gTTS(translated, lang=lang_code)
    output_path = 'static/output_dubbed_audio.mp3'
    tts.save(output_path)

    return render_template('result.html')

