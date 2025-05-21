import yt_dlp
import sys
import os

def download_audio(youtube_url, output_path='downloads'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python download_audio.py <YouTube_URL>")
    else:
        youtube_url = sys.argv[1]
        download_audio(youtube_url)

