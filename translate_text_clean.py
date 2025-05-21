import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TARGET_LANG = os.getenv("TARGET_LANG", "Telugu")

with open("downloads/audio_transcript.txt", "r") as f:
    input_text = f.read()

prompt = f"Translate this English transcript to {TARGET_LANG} in natural spoken style:\n\n{input_text}"

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="gpt-3.5-turbo"
)

output_text = chat_completion.choices[0].message.content

with open("downloads/translated_output.txt", "w") as f:
    f.write(output_text)

print("✅ Translation complete. Saved to downloads/translated_output.txt")

