import serial
import sounddevice as sd
import numpy as np
import whisper
#from server import ser 

# Initialize Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(audio_data):
    audio_float = audio_data.astype(np.float32) / np.iinfo(np.int16).max
    audio_np = np.hstack(audio_float)
    result = model.transcribe(audio_np, verbose=Fa.lse)
    print(result['text'])
    return result['text']
    

# Initialize serial communication with Arduino
#ser = serial.Serial('COM5', 9600)  # Replace 'COM5' with your Arduino's COM port

# Function to record audio
def record_audio():
    print("Recording...")
    audio_data = []
    with sd.InputStream(samplerate=16000, channels=1, dtype='int16') as stream:
        while True:
            frame, overflowed = stream.read(1024)
            audio_data.append(frame)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line == "RECORD_STOP":
                    audio_data = np.concatenate(audio_data)
                    print("Recording stopped, transcribing...")
                    return audio_data

# Main loop to listen for signals from Arduino
if __name__ == "__main__":
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "RECORD_START":
                audio_data = record_audio()
                text = transcribe_audio(audio_data)
                print("Transcribed Text: {text}")
