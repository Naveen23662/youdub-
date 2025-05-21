import whisper

model = whisper.load_model("base")  # You can try "small" or "medium" if needed
result = model.transcribe("audio.mp3")

print("\n📝 Transcription Result:\n")
print(result["text"])

