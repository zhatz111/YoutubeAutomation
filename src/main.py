"""_summary_
"""
from video_downloader import tiktok_downloader # pylint: disable=import-error
from closed_captions import forced_align, main # pylint: disable=import-error
from text_speech import generate_speech # pylint: disable=import-error

# Variables that need to be changed for each new video
TIKTOK_URL = "https://www.tiktok.com/@funnyanimal319/video/7289089427132009761"
VIDEO_OUTPUT_NAME = "vid_7_12232023"

# Variaales that should be left alone unless changing download directory or
# script location
DOWNLOAD_DIR = r"C:\Users\zhatz\Documents\GitHub\YoutubeAutomation\Videos"
VIDEO_SCRIPT = "text/video_script.txt"
AUDIO_FILE_PATH = f"Audio/{VIDEO_OUTPUT_NAME}"

voices = [
    {"voice_id": "mZ8gt3O1VRrVHQ9eD5M6", "name": "Neil"},
    {"voice_id": "BCIFybqsHwndhbJ6VRqL", "name": "Dann"},
    {"voice_id": "bnEwjkD4Bh7zQ4PGuPRB", "name": "Gault"},
    {"voice_id": "ErXwobaYiN019PkySvjV", "name": "Antoni"},
    {"voice_id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli"},
    {"voice_id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh"},
    {"voice_id": "VR6AewLTigWG4xSOukaG", "name": "Arnold"},
    {"voice_id": "pNInz6obpgDQGcFmaJgB", "name": "Adam"},
    {"voice_id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam"},
    {"voice_id": "soelvv1eItXKyaOcH89G", "name": "Mark"},
    {"voice_id": "G7paNAs8Wo434Eezb936", "name": "Harry"}
]

video_file_path = tiktok_downloader(
    tiktok_url=TIKTOK_URL,
    download_dir=DOWNLOAD_DIR,
)

generate_speech(
    api_key_path = "data/api_key.txt",
    text_file_path = VIDEO_SCRIPT,
    output_filename = AUDIO_FILE_PATH,
    voice_id = "bnEwjkD4Bh7zQ4PGuPRB",
)

forced_align(
    audio_file_path = f"{AUDIO_FILE_PATH}.mp3",
    subtitle_json_path = "text/text_data.json",
    model_type = "medium",
)

main(
    input_video_path = video_file_path,
    speech_audio_path = f"{AUDIO_FILE_PATH}.mp3",
    video_output_path = f"Videos/{VIDEO_OUTPUT_NAME}.mp4",
    subtitle_json_path = "text/text_data.json",
    font ="fonts/burbankbig_fortnite.ttf",
    fontsize = 100,
    color = "white",
    stroke_color = "black",
    bgcolor = "#75BFEC",
    stroke_size = 5,
    y_position = 500,
    frame_size = (1080, 1920),
    volume = 0.2,
    fps = 30,
    codec = "libx264",
    audio_codec = "libmp3lame",
)
