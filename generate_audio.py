import os
import edge_tts
import asyncio

# Load translated text
with open("translated_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Choose a TTS voice (for Telugu, female)
VOICE = "te-IN-ShrutiNeural"  # You can change to another

# Output file name
OUTPUT_FILE = "output_audio.mp3"

async def text_to_speech():
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

asyncio.run(text_to_speech())

print("✅ Dubbed audio generated:", OUTPUT_FILE)

