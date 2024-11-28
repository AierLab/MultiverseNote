# %%
import time
import requests
from midi2audio import FluidSynth
from IPython.display import Audio, display

class TextToMidiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def submit_text(self, text):
        url = f"{self.base_url}/submit-text"
        headers = {'Content-Type': 'application/json'}
        data = {'text': text}

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def check_status(self, job_id):
        url = f"{self.base_url}/check-status/{job_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_result(self, job_id):
        url = f"{self.base_url}/get-result/{job_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def download_midi(self, job_id, save_path):
        url = f"{self.base_url}/download-midi/{job_id}"
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
    
# Initialize the client with the base URL of your Flask server
text2midi_client = TextToMidiClient(base_url="http://localhost:5000")


# %%
# Define an assistant tool to handle music conversion
def convert_text_to_midi(text_command):
    try:
        # Step 1: Submit text for MIDI conversion
        submit_response = text2midi_client.submit_text(text_command)
        job_id = submit_response['jobId']
        print(f"Job submitted. Job ID: {job_id}")

        # Step 2: Poll the job status until it's completed
        while True:
            status_response = text2midi_client.check_status(job_id)
            status = status_response['status']
            # print(f"Job Status: {status}")
            if status == 'completed':
                break
            elif status == 'failed':
                print("Job failed.")
                return None
            time.sleep(10)  # Wait for 2 seconds before checking again

        # Step 3: Retrieve the result (metadata)
        result_response = text2midi_client.get_result(job_id)
        meta_data = result_response['metaData']
        print("Metadata:")
        print(meta_data)

        # Step 4: Download the MIDI file
        midi_file_path = text2midi_client.download_midi(job_id, save_path=f"storage/{job_id}.mid")
        print(f"MIDI file downloaded to {midi_file_path}")

        return midi_file_path, meta_data

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err.response.json()}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

# %%
import threading
import queue
import time
import re

def handle_midi_conversion(text_command, result_queue):
    """Thread function to handle MIDI conversion and store results."""
    midi_result = convert_text_to_midi(text_command)
    result_queue.put(midi_result)  # Place the result in a queue for the main thread to retrieve.

def start(text_command):
    result_queue = queue.Queue()
    conversion_thread = threading.Thread(target=handle_midi_conversion,
                                         args=(text_command, result_queue))
    conversion_thread.start()

# def check_status():
#     # Check if there's a MIDI conversion in progress
#     if conversion_thread and conversion_thread.is_alive():
#         # speakText("MIDI conversion is in progress...")
#         pass
#     else:
#         # If the MIDI conversion has finished, handle the result
#         if conversion_thread and not conversion_thread.is_alive():
#             if not result_queue.empty():
#                 midi_result = result_queue.get()
#                 if midi_result:
#                     midi_file_path, meta_data = midi_result
#                     speakText(f"MIDI file saved successfully.")
#                 else:
#                     speakText("MIDI conversion failed.")
#                 conversion_thread = None  # Reset the thread