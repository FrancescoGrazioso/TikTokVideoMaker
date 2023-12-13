import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import argparse

def split_video(input_path, output_folder, segment_length, add_gameplay, gameplay_path):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the base name of the file without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Load the main video clip
    video_clip = VideoFileClip(input_path)

    # Maximum duration for each segment (in seconds)
    max_segment_duration = 120
    segment_duration = min(segment_length, max_segment_duration) if segment_length else 60

    # Calculate the number of segments
    num_segments = int(video_clip.duration // segment_duration) + 1

    # Divide the video into segments
    video_segments = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, video_clip.duration)
        segment = video_clip.subclip(start_time, end_time)
        video_segments.append(segment)

    # Load the gameplay video if requested
    if add_gameplay:
        if gameplay_path:
            gameplay_clip = VideoFileClip(gameplay_path)
        else:
            gameplay_clip = VideoFileClip("gameplay.mp4")
        gameplay_clip.audio = None
    else:
        gameplay_clip = None

    # Create the output folder
    output_path = os.path.join(output_folder, base_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Compose the segmented videos with gameplay (if present) and save
    for i, segment in enumerate(video_segments):
        if add_gameplay:
            adjusted_gameplay_clip = gameplay_clip.subclip(0, segment.duration)
            output_clip = CompositeVideoClip([segment.set_position(('center', 'top')),
                                              adjusted_gameplay_clip.set_position(('center', 'bottom'))],
                                             size=(segment.size[0], segment.size[1] + adjusted_gameplay_clip.size[1]))
        else:
            output_clip = segment

        output_clip.write_videofile(os.path.join(output_path, f"{base_name}_segment_{i + 1}.mp4"), codec="libx264", audio_codec="aac")

    print("Processing complete. Videos have been saved in the 'output' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split and compose video segments with gameplay.")
    parser.add_argument("-v", "--video", help="Path to the input video file.", required=True)
    parser.add_argument("-l", "--length", type=int, help="Length of each video segment in seconds (default: 60, max: 120).")
    parser.add_argument("-g", "--gameplay", action="store_true", help="Add gameplay video to each segment (default: True).")
    parser.add_argument("-gp", "--gameplay-path", help="Path to the custom gameplay video file.")
    args = parser.parse_args()

    input_path = args.video
    output_folder = "output"
    split_video(input_path, output_folder, args.length, args.gameplay, args.gameplay_path)
