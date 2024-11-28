import queue

import sounddevice as sd
import numpy as np
import openai
import threading
import os
from scipy.io.wavfile import write as wavWrite
from gtts import gTTS
from playsound import playsound

import sounddevice as sd
import queue
import threading
import openai
import time
import json

from app.model.dataModel import RoleEnum
from app.view._baseView import *
from build.lib.app.model.dataModel import MessageModel


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

class SpeechView(BaseView):
    def __init__(self, history_manager: HistoryManager, agent_manager: AgentManager, config_manager: ConfigManager):
        super().__init__(history_manager, agent_manager, config_manager)


    def run(self):
        if self.config_manager.config.view.speech.mic_id is None:
            listAudioDevices()
            sd.default.device = int(input("Select the device index for recording: "))
            self.config_manager.config.view.speech.mic_id = sd.default.device
            self.config_manager.save()
        else:
            sd.default.device = self.config_manager.config.view.speech.mic_id

        # openai.api_key = self.config_manager.config.control.bot.api_key

        bot: BaseBot = self._get_current_bot()

        try:
            while True:
                # Start and stop recording with Enter key
                if input("Press Enter to start recording, or type 'exit' to close: ").lower() == "exit":
                    speakText("Goodbye!")
                    break

                # Record audio input
                audioFile = record_audio()
                user_input = transcribe_audio(audioFile)
                print(f"{"-" * 80}\n{"-" * 80}\nUser: {user_input}")

                if user_input.lower() == 'exit':
                    speakText("Goodbye!")
                    break

                message = MessageModel(role=RoleEnum.USER, content=user_input)
                self.history_manager.add_session_message(message, self.current_session)

                # TODO MOVE INTO THE CONFIG
                agent = self.agent_manager.load("piano_artist")

                response_message = bot.ask(message, self.current_session, agent)
                print(f"{"-" * 80}\nAssistant: {response_message.content}")
                speakText(response_message.content)

        except KeyboardInterrupt:
            speakText("Program exited by user.")

