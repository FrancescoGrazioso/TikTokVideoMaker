import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import cv2

def split_video(input_path, output_folder):
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ottieni il nome del file senza estensione
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Carica il video principale
    video_clip = VideoFileClip(input_path)

    # Durata massima per ciascun segmento (in secondi)
    segment_duration = 60

    # Calcola il numero di segmenti
    num_segments = int(video_clip.duration // segment_duration) + 1

    # Divide il video in segmenti
    video_segments = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, video_clip.duration)
        segment = video_clip.subclip(start_time, end_time)
        video_segments.append(segment)

    # Carica il video di gameplay
    gameplay_clip = VideoFileClip("gameplay.mp4")
    gameplay_clip.audio = None

    # Creazione della cartella di output
    output_path = os.path.join(output_folder, base_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Composizione dei video segmentati con il gameplay e salvataggio
    for i, segment in enumerate(video_segments):
        adjusted_gameplay_clip = gameplay_clip.subclip(0, segment.duration)
        output_clip = CompositeVideoClip([segment.set_position(('center', 'top')),
                                          adjusted_gameplay_clip.set_position(('center', 'bottom'))],
                                         size=(segment.size[0], segment.size[1] + adjusted_gameplay_clip.size[1]))

        output_clip.write_videofile(os.path.join(output_path, f"{base_name}_segment_{i + 1}.mp4"), codec="libx264", audio_codec="aac")

    print("Elaborazione completata. I video sono stati salvati nella cartella 'output'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python script.py path/del/video")
        sys.exit(1)

    input_path = sys.argv[1]
    output_folder = "output"
    split_video(input_path, output_folder)



