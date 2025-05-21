import torchaudio
import torch
import librosa

def detect_gender(audio_path):
    waveform, sr = torchaudio.load(audio_path)
    y = waveform[0].numpy()
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitch = pitch[pitch > 0]

    avg_pitch = pitch.mean()
    print("Average pitch:", avg_pitch)

    # Thresholds (approx):
    if avg_pitch > 160:
        return "female"
    else:
        return "male"

