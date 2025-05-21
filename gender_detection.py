
import torch
import torchaudio
import numpy as np

def detect_gender(audio, sr):
    # Dummy function based on simple energy threshold
    energy = np.mean(np.square(audio))
    return "male" if energy > 0.01 else "female"
