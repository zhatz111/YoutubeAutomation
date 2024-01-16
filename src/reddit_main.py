# This code is a Python script that performs various tasks related to video processing.

import json
from pathlib import Path
from closed_captions import forced_align, main # pylint: disable=import-error
from text_speech import text_to_audio # pylint: disable=import-error, unused-import
from video_merger import video_merger # pylint: disable=import-error, unused-import

# Determine parent path of repository
parent_dir = Path.cwd()

# Variables that need to be changed for each new video
VIDEO_LIST = ["zchoi_vid1", "zchoi_vid2"]
# VIDEO_INPUT_NAME = "zach_choi_asmr_1"
VIDEO_OUTPUT_NAME = "zchoi_merge1"

# Variaales that should be left alone unless changing download directory or
# script location

with open(parent_dir / "data/api_keys.json", encoding="utf-8") as f:
    api_keys = json.load(f)

DOWNLOAD_DIR = parent_dir / "Videos"
VIDEO_SCRIPT = parent_dir / "text/video_script.txt"
AUDIO_FILE_PATH = parent_dir / f"Audio/Reddit_ASMR/{VIDEO_OUTPUT_NAME}.mp3"
CLIENT_INFO = parent_dir / "data/citric-banner-411306-14a6fe3b7d14.json"

# Main functions to download and create video

video_file_path = video_merger(
    input_video_list = VIDEO_LIST,
    parent_path = DOWNLOAD_DIR / "Reddit_ASMR" / "Downloaded_Videos",
    video_output_path = DOWNLOAD_DIR / "Reddit_ASMR" / "Downloaded_Videos" / f"{VIDEO_OUTPUT_NAME}.mp4",
    frame_size = (1080, 1920),
    volume = 1,
    fps = 30,
    codec = "libx264",
    audio_codec = "libmp3lame",
)

# generate_speech_2(
#     api_key = api_keys["voice_api_keys"]["eleven_labs_2"],
#     text_file_path = VIDEO_SCRIPT,
#     output_filename = AUDIO_FILE_PATH,
#     voice_id = api_keys["voice_ids"]["voice_id_2"],
# )

text_to_audio(
    voice_name="en-US-Studio-O",
    text_file=VIDEO_SCRIPT,
    output_filepath=AUDIO_FILE_PATH,
    client_info_path=CLIENT_INFO,
)

forced_align(
    audio_file_path = AUDIO_FILE_PATH,
    subtitle_json_path = parent_dir / "text/text_data.json",
    model_type = "medium",
)

main(
    input_video_path = video_file_path,
    speech_audio_path = AUDIO_FILE_PATH,
    video_output_path = parent_dir / f"Videos/Reddit_ASMR/Final_Videos/{VIDEO_OUTPUT_NAME}.mp4",
    subtitle_json_path = parent_dir / "text/text_data.json",
    font = parent_dir / "fonts/digitalt.ttf",
    fontsize = 110,
    color = "white",
    stroke_color = "black",
    bgcolor = "#00cc00", # #00cc00, #75BFEC
    stroke_size = 3,
    y_position = 500,
    frame_size = (1080, 1920),
    volume = .3,
    fps = 30,
    codec = "libx264",
    audio_codec = "libmp3lame",
)
