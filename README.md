# TikTokVideoMaker

This script allows you to split a video into segments, optionally adding gameplay footage to each segment.

## Prerequisites

- Python 3
- Required Python libraries are listed in `requirements.txt`. Install them using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python script.py -v <input_video_path> [-l <segment_length>] [-g]
```

    -v, --video: Path to the input video file (required).
    -l, --length: Length of each video segment in seconds (default: 60, max: 120).
    -g, --gameplay: Add gameplay video to each segment (default: True).

## Example

```bash

python script.py -v input_video.mp4 -l 45 -g
```

This example splits the video "input_video.mp4" into segments of 45 seconds each, adding gameplay footage to each segment.
Notes

    Ensure that ffmpeg is installed on your system, and the path is correctly set (IMAGEIO_FFMPEG_EXE).
    The script will create an 'output' folder to store the segmented videos.

Feel free to modify the options according to your needs. For additional help, use:

```bash
python script.py -h
```

Note: Adjust the paths and filenames in the script according to your file structure.

This `README.md` provides a brief overview of the script, its usage, and import