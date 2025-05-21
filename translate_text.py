
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
target_lang = os.getenv("TARGET_LANG", "Telugu")

# Initialize OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Read the transcript from file
with open("downloads/audio_transcript.txt", "r") as f:
    original_text = f.read()

# Prompt setup for translation
prompt = f"Translate the following English text to {target_lang}:

{original_text}"

# Make the API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a translation assistant."},
        {"role": "user", "content": prompt}
    ]
)

# Extract response text
translated_text = response.choices[0].message.content.strip()

# Save to file
with open("downloads/audio_transcript_translated.txt", "w") as f:
    f.write(translated_text)

print("✅ Translation complete and saved to downloads/audio_transcript_translated.txt")

