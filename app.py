from flask import Flask, render_template, request, send_file, url_for, after_this_request
import os
import yt_dlp
from deep_translator import GoogleTranslator
from generate_audio_edge import generate_edge_audio
from urllib.parse import urlparse, parse_qs
import openai

# Securely load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_subtitles(url):
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'srt',
        'skip_download': True,
        'quiet': True,
        'outtmpl': f'{UPLOAD_FOLDER}/subs',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    srt_file = os.path.join(UPLOAD_FOLDER, "subs.en.srt")
    if not os.path.exists(srt_file):
        return None
    with open(srt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    text = ""
    for line in lines:
        if line.strip().isdigit() or "-->" in line:
            continue
        text += line.strip() + " "
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download_and_dub():
    url = request.form['url']
    target_lang = request.form['language']

    transcript = get_subtitles(url)
    if not transcript:
        transcript = "This video has no subtitles, so this is a default intro by YouDub."

    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(transcript)

    audio_output = os.path.join(UPLOAD_FOLDER, "dubbed_audio.mp3")
    generate_edge_audio(translated_text, audio_output, target_lang)

    video_path = os.path.join(UPLOAD_FOLDER, "video.mp4")
    video_opts = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': video_path,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(video_opts) as ydl:
        ydl.download([url])

    final_output = os.path.join(UPLOAD_FOLDER, "final_dubbed_video.mp4")
    os.system(f'ffmpeg -y -i "{video_path}" -i "{audio_output}" -c:v copy -c:a aac -strict experimental "{final_output}"')

    @after_this_request
    def cleanup(response):
        try:
            os.remove(audio_output)
            os.remove(video_path)
            if os.path.exists(f'{UPLOAD_FOLDER}/subs.en.srt'):
                os.remove(f'{UPLOAD_FOLDER}/subs.en.srt')
        except Exception as e:
            print("Cleanup error:", e)
        return response

    return render_template("result.html", video_file="final_dubbed_video.mp4")

# ✅ For Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

