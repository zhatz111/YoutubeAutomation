
import os
from pathlib import Path
from moviepy.editor import (  # pylint: disable=import-error
    VideoFileClip,
    concatenate_videoclips
)

def video_merger(
    input_video_list: list,
    parent_path: Path,
    video_output_path: str,
    frame_size: tuple = (1080, 1920),
    volume: int = 1,
    fps: int = 30,
    codec: str = "libx264",
    audio_codec: str = "libmp3lame",
):
    vid_dir = os.listdir(parent_path)
    if video_output_path.name in vid_dir:
        print("Using existing Video file!")
        return video_output_path

    # Load the input video
    input_videos = [VideoFileClip(str(parent_path / f"{x}.mp4")) for x in input_video_list]
    for video in input_videos:
        if video.size[0] != frame_size[0]:
            video = video.resize( # pylint: disable=no-member
                width=frame_size[0]
            )

    trimmed_clips = []
    for i, clip in enumerate(input_videos):
        # Duration of the clip minus 3 seconds
        trimmed_duration = clip.duration - 2
        # Trim the last 3 seconds
        trimmed_clip = clip.subclip(0, trimmed_duration)
        # Save the trimmed clip (optional)
        trimmed_clip.write_videofile(f"{input_video_list[i]}.mp4", codec=codec, audio_codec=audio_codec)
        # Add the trimmed clip to the list (optional)
        trimmed_clips.append(trimmed_clip)

    for video in trimmed_clips:
        # video = video.cutout(video.duration - 3, video.duration)
        video = video.volumex(volume)

    print("Merging Videos Together...")
    # If you want to overlay this on the original video uncomment this and
    # also change frame_size, font size and color accordingly.
    merged_video = concatenate_videoclips(trimmed_clips, method="compose")

    # Save the final clip as a video file with the audio included
    merged_video.write_videofile(
        str(video_output_path),
        fps=fps,
        codec=codec,
        audio_codec=audio_codec,
    )

    return video_output_path
