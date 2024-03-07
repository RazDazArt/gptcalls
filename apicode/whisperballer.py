# whisper_integration.py
import sounddevice as sd
import numpy as np
import whisper

model = whisper.load_model("base")

def transcribe_audio(duration=5):  # Duration in seconds
    def callback(indata, frames, time, status):
        # This callback shouldn't do anything in this simplified example
        pass

    with sd.InputStream(callback=callback, samplerate=16000, channels=1, dtype='int16') as stream:
        print("Recording...")
        audio = sd.rec(int(duration * stream.samplerate), samplerate=16000, channels=1, dtype='int16')
        sd.wait()
        print("Recording stopped, transcribing...")

    audio_float = audio.astype(np.float32) / np.iinfo(np.int16).max
    audio_np = np.hstack(audio_float)
    result = model.transcribe(audio_np, verbose=False)
    return result['text']