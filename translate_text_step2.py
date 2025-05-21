import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Read the transcript
with open("downloads/audio_transcript.txt", "r") as f:
    input_text = f.read()

# Translate to Telugu
prompt = f"Translate this English text to Telugu:\n\n{input_text}"

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a translator."},
        {"role": "user", "content": prompt}
    ]
)

translated_text = response.choices[0].message.content

# Save the output
with open("downloads/translated_output.txt", "w") as f:
    f.write(translated_text)

print("✅ Translation completed and saved to downloads/translated_output.txt")

