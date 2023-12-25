'''The `generate_speech` function sends a request to a text-to-speech API with a specified voice and
saves the generated speech to an output file.

Parameters
----------
api_key_path
    The `api_key_path` parameter is the path to the file that contains your API key for the
text-to-speech service. This API key is required to authenticate your requests to the API and access
the text-to-speech functionality.
text_file_path : str
    The `text_file_path` parameter is the path to the text file that contains the text you want to
convert to speech. This file should be a plain text file with the content you want to convert.
output_filename : str
    The `output_filename` parameter is the name of the output file that will contain the generated
speech. It should be a string value. For example, if you want the output file to be named
"speech_output", you would pass "speech_output" as the value for the `output_filename` parameter
voice_id : str, optional
    The `voice_id` parameter is a unique identifier for a specific voice. It is used to specify the
voice that will be used for generating the speech. In the given code, the default `voice_id` is set
to "soelvv1eItXKyaOcH89G

'''

import os
import json
from pathlib import Path
import http.client

# Function to send a request to the API and save the speech
def generate_speech(
    api_key,
    text_file_path: Path,
    output_filename: Path,
    voice_id: str,
):
    '''The function `generate_speech` generates speech from a text file using a specified voice and saves
    it to an output file.
    
    Parameters
    ----------
    api_key_path
        The path to the file containing your API key for the text-to-speech service.
    text_file_path : str
        The path to the text file that contains the text you want to convert to speech.
    output_filename : str
        The name of the output file that will contain the generated speech.
    voice_id : str, optional
        The `voice_id` parameter is used to specify the voice that will be used for generating the speech.
    It is a unique identifier for a specific voice.
    
    '''
    # Default voice_id is Mark, but change this if needed
    # try:
    #     with open(api_key_path, "r", encoding="utf-8") as file:
    #         api_key = file.read().strip()
    # except FileNotFoundError:
    #     print("API key file not found!")
    audio_dir = os.listdir(str(output_filename.parent))
    if f"{output_filename.name}.mp3" in audio_dir:
        print("Using existing audio file.")
        return

    try:
        with open(str(text_file_path), "r", encoding="utf-8") as file:
            text = file.read().strip()
    except FileNotFoundError:
        print("Text file not found!")

    # API endpoint
    conn = http.client.HTTPSConnection("api.elevenlabs.io")

    # Request headers
    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }

    # Request payload
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0, "similarity_boost": 0},
    }

    # Send POST request to the API
    conn.request(
        "POST",
        f"/v1/text-to-speech/{voice_id}?optimize_streaming_latency=0",
        headers=headers,
        body=json.dumps(payload),
    )

    # Get the response
    response = conn.getresponse()

    # Check if the request was successful
    if response.status == 200:
        # Save the audio file
        with open(f"{output_filename}.mp3", "wb") as file:
            file.write(response.read())
        print("Speech generated successfully!")
    else:
        print("Error:", response.status)

    # Close the connection
    conn.close()
