import json
import http.client


# Function to send a request to the API and save the speech
def generate_speech(
    api_key_path,
    text_file_path: str,
    output_filename: str,
    voice_id: str = "soelvv1eItXKyaOcH89G",
):
    """_summary_

    Args:
        api_key (_type_): _description_
        text (_type_): _description_
        voice_id (_type_): _description_
        output_filename (_type_): _description_
    """
    # Default voice_id is Mark, but change this if needed

    try:
        with open(api_key_path, "r", encoding="utf-8") as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        print("API key file not found!")

    try:
        with open(text_file_path, "r", encoding="utf-8") as file:
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
