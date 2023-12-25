"""
The code is importing the `Path` class from the `pathlib` module and the `youtube_upload` function
from the `youtube_uploader` module.
The script runs the youtube_upload function to upload a video to a youtube channel.
All the video metadata is stored in a JSON file that is read in.
"""

from pathlib import Path
from youtube_uploader import youtube_upload # pylint: disable=import-error

# Determine parent path of repository
parent_dir = Path.cwd()
METADATA_PATH = parent_dir / "data/video_upload_metadata.json"

youtube_upload(METADATA_PATH)
