"""_summary_

Returns:
    _type_: _description_
"""
import json
import whisper # pylint: disable=import-error
from moviepy.editor import ( # pylint: disable=import-error
    TextClip,
    CompositeVideoClip,
    VideoFileClip,
    CompositeAudioClip,
    AudioFileClip,
    ColorClip,
)

def forced_align(audio_file_path: str, subtitle_json_path: str, model_type: str = "medium"):
    """_summary_

    Args:
        audio_file_path (str): _description_
        model_type (str, optional): _description_. Defaults to "medium".
    """
    model = whisper.load_model(model_type)
    print("Transcribing Audio with word timestamps...")
    result = model.transcribe(audio_file_path, word_timestamps=True)

    print("Writing timestamped text data to json...")
    wordlevel_info = []
    for each in result["segments"]:
        words = each["words"]
        for word in words:
            wordlevel_info.append(
                {"word": word["word"].strip(), "start": word["start"], "end": word["end"]}
            )

    with open(subtitle_json_path, "w", encoding="utf-8") as f:
        json.dump(wordlevel_info, f, indent=4)

def split_text_into_lines(data):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    max_chars = 8
    # max_duration in seconds
    max_duration = 3.0
    # Split if nothing is spoken (gap) for these many seconds
    max_gap = 1.5

    subtitles = []
    line = []
    line_duration = 0

    for idx, word_data in enumerate(data):
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)

        # Check if adding a new word exceeds the maximum character count or duration
        new_line_chars = len(temp)

        duration_exceeded = line_duration > max_duration
        chars_exceeded = new_line_chars > max_chars
        if idx > 0:
            gap = word_data["start"] - data[idx - 1]["end"]  # start of next word, end of last word time gap
            max_gap_exceeded = gap > max_gap
        else:
            max_gap_exceeded = False

        if duration_exceeded or chars_exceeded or max_gap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line,
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0

    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line,
        }
        subtitles.append(subtitle_line)

    return subtitles

def create_caption(
    text_json,
    framesize,
    font="fonts/burbankbig_fortnite.ttf",
    fontsize=120,
    color="white",
    stroke_color="black",
    bgcolor="#FF5733",
    stroke_size=5,
):
    """_summary_

    Args:
        text_json (_type_): _description_
        framesize (_type_): _description_
        font (str, optional): _description_. Defaults to "fonts/burbankbig_fortnite.ttf".
        fontsize (int, optional): _description_. Defaults to 120.
        color (str, optional): _description_. Defaults to "white".
        stroke_color (str, optional): _description_. Defaults to "black".
        bgcolor (str, optional): _description_. Defaults to "#FF5733".
        stroke_size (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: _description_
    """

    full_duration = text_json["end"] - text_json["start"]
    word_clips = []
    xy_textclips_positions = []

    # x_pos = 180
    # y_pos = 500

    frame_width = framesize[0]
    frame_height = framesize[1]
    x_buffer = frame_width * 1 / 10
    y_buffer = frame_height * 1 / 5
    space_width = ""

    for _ in text_json["textcontents"]:
        phrase_length = 0
        for word_json in text_json["textcontents"]:
            word_clip_test = (
            TextClip(
                word_json["word"],
                font=font,
                fontsize=fontsize,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_size,
            )
            .set_start(text_json["start"])
            .set_duration(full_duration)
        )
            phrase_length += word_clip_test.size[0]

        phrase_length += (len(text_json["textcontents"])- 1)*20
        x_pos = (frame_width/2) - (phrase_length/2)
        y_pos = 500

        for _, word_json in enumerate(text_json["textcontents"]): # change back to textcontents
            duration = word_json["end"] - word_json["start"]
            word_clip = (
                TextClip(
                    word_json["word"],
                    font=font,
                    fontsize=fontsize,
                    color=color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_size,
                )
                .set_start(text_json["start"])
                .set_duration(full_duration)
            )

            frame_height = framesize[1]
            word_clip_space = (
                TextClip(" ", font=font, fontsize=fontsize, color=color)
                .set_start(text_json["start"])
                .set_duration(full_duration)
            )
            word_width, word_height = word_clip.size
            space_width, _ = word_clip_space.size

            if x_pos + word_width + space_width > frame_width - 1.3 * x_buffer:
                # Move to the next line
                y_pos = y_pos + word_height + 40

                # Store info of each word_clip created
                xy_textclips_positions.append(
                    {
                        "x_pos": x_pos,
                        "y_pos": y_pos + y_buffer,
                        "width": word_width,
                        "height": word_height,
                        "word": word_json["word"],
                        "start": word_json["start"],
                        "end": word_json["end"],
                        "duration": duration,
                    }
                )

                word_clip = word_clip.set_position((x_pos, y_pos + y_buffer))
                word_clip_space = word_clip_space.set_position(
                    (x_pos + word_width, y_pos + y_buffer)
                )
                x_pos = word_width + space_width
            else:
                # Store info of each word_clip created
                xy_textclips_positions.append(
                    {
                        "x_pos": x_pos,
                        "y_pos": y_pos + y_buffer,
                        "width": word_width,
                        "height": word_height,
                        "word": word_json["word"],
                        "start": word_json["start"],
                        "end": word_json["end"],
                        "duration": duration,
                    }
                )

                word_clip = word_clip.set_position((x_pos, y_pos + y_buffer))
                word_clip_space = word_clip_space.set_position(
                    (x_pos + word_width, y_pos + y_buffer)
                )
                x_pos = x_pos + word_width + space_width

            word_clips.append(word_clip)
            word_clips.append(word_clip_space)

        for highlight_word in xy_textclips_positions:
            word_clip_highlight = (
                TextClip(
                    highlight_word["word"],
                    font=font,
                    fontsize=fontsize,
                    color=bgcolor,
                    stroke_color=stroke_color,
                    stroke_width=stroke_size,
                )
                .set_start(highlight_word["start"])
                .set_duration(highlight_word["duration"])
            )
            word_clip_highlight = word_clip_highlight.set_position(
                (highlight_word["x_pos"] + 2, highlight_word["y_pos"] + 1)
            )
            word_clips.append(word_clip_highlight)

    return word_clips


def main(
    input_video_path: str,
    speech_audio_path: str,
    video_output_path: str,
    subtitle_json_path: str,
    font: str ="fonts/burbankbig_fortnite.ttf",
    fontsize: int = 120,
    color: str = "white",
    stroke_color: str = "black",
    bgcolor: str = "#FF5733",
    stroke_size: int = 5,
    frame_size: tuple = (1080, 1920),
    volume: int = 1,
    fps: int = 30,
    codec: str = "libx264",
    audio_codec: str = "libmp3lame",
):
    """_summary_"""

    with open(subtitle_json_path, "r", encoding="utf-8") as f:
        wordlevel_info_modified = json.load(f)

    print("Splitting text and generating captions...")
    linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)
    all_linelevel_splits = []
    for line in linelevel_subtitles:
        out = create_caption(
            line,
            frame_size,
            font,
            fontsize,
            color,
            stroke_color,
            bgcolor,
            stroke_size,
            )
        all_linelevel_splits.extend(out)

    # Load the input video
    input_video = VideoFileClip(input_video_path)
    input_video = input_video.volumex(volume)
    print("Compositing final video...")
    # If you want to overlay this on the original video uncomment this and
    # also change frame_size, font size and color accordingly.
    background_clip = ColorClip(size=frame_size, color=(0, 0, 0)).set_duration(input_video.duration)
    final_video = CompositeVideoClip([background_clip, input_video] + all_linelevel_splits)
    audioclip = AudioFileClip(speech_audio_path)
    new_audioclip = CompositeAudioClip([input_video.audio, audioclip])

    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(new_audioclip)

    # Save the final clip as a video file with the audio included
    final_video.write_videofile(
        video_output_path, fps=fps, codec=codec, audio_codec=audio_codec,
    )
