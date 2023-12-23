"""_summary_

Returns:
    _type_: _description_
"""
import json
import whisper  # pylint: disable=import-error
from moviepy.editor import (  # pylint: disable=import-error
    TextClip,
    CompositeVideoClip,
    VideoFileClip,
    CompositeAudioClip,
    AudioFileClip,
    ImageClip,
)


def forced_align(
    audio_file_path: str, subtitle_json_path: str, model_type: str = "medium"
):
    """The function `forced_align` takes an audio file path, a subtitle JSON file path, and an optional
    model type as input, transcribes the audio file with word timestamps using the specified model, and
    writes the timestamped text data to the subtitle JSON file.

    Parameters
    ----------
    audio_file_path : str
        The path to the audio file that you want to transcribe and align with subtitles.
    subtitle_json_path : str
        The `subtitle_json_path` parameter is the file path where you want to save the JSON file containing
    the word-level information (word, start time, end time) of the transcribed audio.
    model_type : str, optional
        The `model_type` parameter is used to specify the type of pre-trained model to use for
    transcription. It has a default value of "medium", but you can pass different values to use
    different models. The available options depend on the library you are using for transcription (e.g.,
    Whisper, Deep

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
                {
                    "word": word["word"].strip(),
                    "start": word["start"],
                    "end": word["end"],
                }
            )

    with open(subtitle_json_path, "w", encoding="utf-8") as f:
        json.dump(wordlevel_info, f, indent=4)


def split_text_into_lines(data):
    """The function `split_text_into_lines` takes in a list of word data and splits it into lines based on
    maximum character count, maximum duration, and maximum gap between words.

    Parameters
    ----------
    data
        The `data` parameter is a list of dictionaries, where each dictionary represents a word in the
    text. Each dictionary has the following keys:

    Returns
    -------
        a list of subtitle lines. Each subtitle line is a dictionary containing the following keys: "word"
    (the concatenated words in the line), "start" (the start time of the line), "end" (the end time of
    the line), and "textcontents" (a list of word data for each word in the line).

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
            gap = (
                word_data["start"] - data[idx - 1]["end"]
            )  # start of next word, end of last word time gap
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
    y_position=500,
):
    """The function `create_caption` takes in various parameters such as `text_json`, `framesize`, `font`,
    `fontsize`, `color`, `stroke_color`, `bgcolor`, `stroke_size`, and `y_position` to create a caption
    for an image or video frame.

    Parameters
    ----------
    text_json
        The text_json parameter is a JSON object that contains the text to be displayed in the caption. It
    should have the following structure:
    framesize
        The framesize parameter specifies the size of the caption frame. It determines the width and height
    of the caption frame in pixels.
    font, optional
        The font parameter specifies the path to the font file that will be used for the caption text. In
    this case, it is set to "fonts/burbankbig_fortnite.ttf".
    fontsize, optional
        The fontsize parameter determines the size of the text in the caption. It is set to 120 by default.
    color, optional
        The color parameter specifies the color of the text. It can be any valid color value, such as
    "red", "#FF5733", or "rgb(255, 87, 51)".
    stroke_color, optional
        The stroke_color parameter is used to specify the color of the stroke or outline around the text.
    bgcolor, optional
        The bgcolor parameter is used to specify the background color of the caption. It takes a
    hexadecimal color code as input. In this case, the default value is "#FF5733", which represents a
    shade of orange.
    stroke_size, optional
        The stroke_size parameter determines the size of the stroke or outline around the text. It is set
    to 5 by default, but you can adjust it to your desired value.
    y_position, optional
        The y_position parameter determines the vertical position of the caption on the image or video
    frame. It specifies the distance in pixels from the top of the frame where the caption will be
    placed.

    """

    full_duration = text_json["end"] - text_json["start"]
    word_clips = []
    xy_textclips_positions = []

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

        phrase_length += (len(text_json["textcontents"]) - 1) * 20

        x_pos = (frame_width / 2) - (phrase_length / 2)
        y_pos = y_position

        for _, word_json in enumerate(
            text_json["textcontents"]
        ):  # change back to textcontents
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
    font: str = "fonts/burbankbig_fortnite.ttf",
    fontsize: int = 120,
    color: str = "white",
    stroke_color: str = "black",
    bgcolor: str = "#FF5733",
    stroke_size: int = 5,
    y_position: int = 500,
    frame_size: tuple = (1080, 1920),
    volume: int = 1,
    fps: int = 30,
    codec: str = "libx264",
    audio_codec: str = "libmp3lame",
):
    """The main function takes in various parameters to create a video with subtitles and audio.

    Parameters
    ----------
    input_video_path : str
        The path to the input video file.
    speech_audio_path : str
        The path to the audio file containing the speech or dialogue that you want to add as subtitles to
    the video.
    video_output_path : str
        The path where the output video will be saved.
    subtitle_json_path : str
        The path to the JSON file containing the subtitles for the video.
    font : str, optional
        The `font` parameter is a string that specifies the path to the font file to be used for the
    subtitles. The default value is set to "fonts/burbankbig_fortnite.ttf".
    fontsize : int, optional
        The `fontsize` parameter is an integer that represents the size of the font used for the subtitles
    in the video.
    color : str, optional
        The color parameter is used to specify the color of the text in the subtitles. It can be any valid
    color name (e.g., "red", "blue", "green") or a hexadecimal color code (e.g., "#FF5733"). The default
    value is "white".
    stroke_color : str, optional
        The `stroke_color` parameter is used to specify the color of the stroke or outline around the text
    in the video. It is a string value that represents the color in any valid CSS color format, such as
    "black", "#000000", or "rgb(0, 0, 0
    bgcolor : str, optional
        The `bgcolor` parameter is used to specify the background color of the subtitle text. It should be
    a hexadecimal color code.
    stroke_size : int, optional
        The `stroke_size` parameter determines the size of the stroke or outline around the text in the
    subtitle. It is an integer value that represents the thickness of the stroke in pixels.
    y_position : int, optional
        The `y_position` parameter determines the vertical position of the subtitles on the video frame. It
    specifies the number of pixels from the top of the frame where the subtitles will be placed.
    frame_size : tuple
        The frame_size parameter is a tuple that specifies the width and height of the video frame. The
    first value in the tuple represents the width of the frame, and the second value represents the
    height of the frame.
    volume : int, optional
        The volume parameter determines the volume level of the speech audio in the final video. It is an
    integer value ranging from 0 to 10, where 0 represents mute and 10 represents maximum volume.
    fps : int, optional
        The "fps" parameter specifies the frames per second (fps) of the output video. It determines how
    many frames are displayed per second in the video.
    codec : str, optional
        The codec parameter specifies the video codec to be used for encoding the output video. In this
    case, the value "libx264" indicates that the H.264 codec will be used.
    audio_codec : str, optional
        The audio codec parameter specifies the codec to be used for encoding the audio in the output
    video. In this case, the "libmp3lame" codec is used, which is a popular codec for encoding audio in
    the MP3 format.

    """

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
            y_position,
        )
        all_linelevel_splits.extend(out)

    # Load the input video
    input_video = VideoFileClip(input_video_path)
    if input_video.size[0] != frame_size[0]:
        input_video = input_video.resize( # pylint: disable=no-member
            width=frame_size[0]
        )
    input_video = input_video.volumex(volume)
    print("Compositing final video...")
    # If you want to overlay this on the original video uncomment this and
    # also change frame_size, font size and color accordingly.
    background_clip = ImageClip("Photos/default_bg_image.png").set_duration(
        input_video.duration
    )
    final_video = CompositeVideoClip(
        [background_clip, input_video.set_position("center")] + all_linelevel_splits
    )
    audioclip = AudioFileClip(speech_audio_path)
    new_audioclip = CompositeAudioClip([input_video.audio, audioclip])

    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(new_audioclip)

    # Save the final clip as a video file with the audio included
    final_video.write_videofile(
        video_output_path,
        fps=fps,
        codec=codec,
        audio_codec=audio_codec,
    )
