import edge_tts
import asyncio
import os

segments = [
    {"speaker": "SPEAKER_0", "text": "Hello, how are you?"},
    {"speaker": "SPEAKER_1", "text": "I'm great, thank you!"},
]

SPEAKER_VOICE_MAP = {
    "SPEAKER_0": "hi-IN-PrabhatNeural",
    "SPEAKER_1": "hi-IN-NeerjaNeural",
}

async def generate_tts_lines():
    if not os.path.exists("tts_segments"):
        os.makedirs("tts_segments")

    for i, segment in enumerate(segments):
        text = segment["text"].strip()
        if not text:
            continue  # Skip empty lines

        voice = SPEAKER_VOICE_MAP.get(segment["speaker"], "hi-IN-PrabhatNeural")
        output_file = f"tts_segments/line_{i}.mp3"

        try:
            tts = edge_tts.Communicate(text=text, voice=voice)
            await tts.save(output_file)
            print(f"✅ Saved: {output_file}")
        except Exception as e:
            print(f"❌ Failed to generate {output_file}: {e}")

if __name__ == "__main__":
    asyncio.run(generate_tts_lines())

