# This code is a Python script that performs various tasks related to video processing.

import json
from pathlib import Path
from video_downloader import tiktok_downloader # pylint: disable=import-error
from closed_captions import forced_align, main # pylint: disable=import-error
from text_speech import generate_speech # pylint: disable=import-error

# Determine parent path of repository
parent_dir = Path.cwd()

# Variables that need to be changed for each new video
<<<<<<< HEAD
TIKTOK_URL = "https://www.tiktok.com/@rubirobelo/video/7310773934952041771"
VIDEO_OUTPUT_NAME = "vid_15_12262023"
=======
TIKTOK_URL = "https://www.instagram.com/reel/CzTQh4XBsJU"
VIDEO_OUTPUT_NAME = "vid_17_12262023"
>>>>>>> 34804e2bc6fa964dc9df36dcc5bef199ee0aaf6a

# Variaales that should be left alone unless changing download directory or
# script location

with open(parent_dir / "data/api_keys.json", encoding="utf-8") as f:
    api_keys = json.load(f)

DOWNLOAD_DIR = parent_dir / "Videos"
VIDEO_SCRIPT = parent_dir / "text/video_script.txt"
AUDIO_FILE_PATH = parent_dir / f"Audio/{VIDEO_OUTPUT_NAME}"

# Main functions to download and create video

video_file_path = tiktok_downloader(
    tiktok_url=TIKTOK_URL,
    download_dir=DOWNLOAD_DIR,
)

generate_speech(
    api_key = api_keys["voice_api_keys"]["eleven_labs_3"],
    text_file_path = VIDEO_SCRIPT,
    output_filename = AUDIO_FILE_PATH,
    voice_id = api_keys["voice_ids"]["voice_id_3"],
)

forced_align(
    audio_file_path = parent_dir / f"{AUDIO_FILE_PATH}.mp3",
    subtitle_json_path = parent_dir / "text/text_data.json",
    model_type = "medium",
)

main(
    input_video_path = video_file_path,
    speech_audio_path = parent_dir / f"{AUDIO_FILE_PATH}.mp3",
    video_output_path = parent_dir / f"Videos/{VIDEO_OUTPUT_NAME}.mp4",
    subtitle_json_path = parent_dir / "text/text_data.json",
    font = parent_dir / "fonts/digitalt.ttf",
    fontsize = 100,
    color = "white",
    stroke_color = "black",
    bgcolor = "#00cc00", # #00cc00, #75BFEC
    stroke_size = 5,
    y_position = 700,
    frame_size = (1080, 1920),
<<<<<<< HEAD
    volume = 0.5,
=======
    volume = 0.6,
>>>>>>> 34804e2bc6fa964dc9df36dcc5bef199ee0aaf6a
    fps = 30,
    codec = "h264_nvenc",
    audio_codec = "libmp3lame",
)
