from app.main import main

if __name__ == "__main__":
    main('storage/config/main_config.yaml')

import sounddevice as sd
import numpy as np
import openai
import threading
import os
from scipy.io.wavfile import write as wavWrite
from gtts import gTTS
from playsound import playsound

def listAudioDevices():
    print(sd.query_devices())

def record_audio(filename='storage/tmp/input.wav', fs=44100):
    """
    Records audio to a WAV file, starting and stopping with Enter key press.
    
    Args:
    filename (str): Path to save the recorded audio file.
    fs (int): Sampling rate in Hz.
    """
    
    def callback(indata, frames, time, status):
        """Callback function called by sounddevice for each audio block."""
        recording.append(indata.copy())  # Append current block of data to the recording list

    def listenForStop():
        """Listens for the Enter key press to stop recording."""
        input("Press Enter again to stop recording...\n")
        nonlocal recordingActive
        recordingActive = False
    
    print("Recording... Press Enter to stop.")
    recordingActive = True
    recording = []

    # Start the thread to listen for Enter key
    stopThread = threading.Thread(target=listenForStop)
    stopThread.start()
    
    with sd.InputStream(callback=callback, dtype='float32', channels=1, samplerate=fs):
        while recordingActive:
            pass

    stopThread.join()  # Ensure the thread is properly closed

    if recording:
        # Concatenate all recorded frames
        recordingArray = np.concatenate(recording, axis=0)
        print("Recording complete.")

        # Normalize and convert to 16-bit integers
        recordingInt = np.int16(recordingArray / np.max(np.abs(recordingArray)) * 32767)
        wavWrite(filename, fs, recordingInt)
        print(f"Audio written to {filename}")
    else:
        print("No audio data recorded.")
    
    return filename

def transcribe_audio(audio_file_path):
    audio_file = open(audio_file_path, "rb")
    transcript = openai.audio.transcriptions.create(
        file=audio_file, 
        model="whisper-1",
        language="en",
        prompt="english back with prompt like expansion"
        )
    return transcript.text

def speakText(text):
    """Converts text to speech and plays it."""
    tts = gTTS(text=text, lang='en')
    tmpPath = "storage/tmp/response_audio.mp3"
    tts.save(tmpPath)
    # https://stackoverflow.com/questions/69245722/error-259-on-python-playsound-unable-to-sound
    playsound(tmpPath)
    os.remove(tmpPath)