import os
import subprocess

def merge_tts_segments(input_folder="tts_segments", output_file="output_dubbed_audio.mp3"):
    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".mp3")])
    
    with open("file_list.txt", "w") as f:
        for file in files:
            f.write(f"file '{input_folder}/{file}'\n")

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_file]
    subprocess.run(cmd)

    os.remove("file_list.txt")
    print(f"\n✅ Final dubbed audio saved to: {output_file}")

if __name__ == "__main__":
    merge_tts_segments()

