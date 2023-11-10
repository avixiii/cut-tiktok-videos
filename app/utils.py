import os
from moviepy.editor import *
from PyQt5.QtWidgets import QFileDialog, QTableWidget
from moviepy.editor import VideoFileClip
import textwrap
import threading

def open_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", "", options=options)

    if folder_path:
        return folder_path


def get_video_info(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith((".mp4", ".avi"))]
    video_info = []

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        clip = VideoFileClip(video_path)
        duration = clip.duration
        width, height = clip.size
        aspect_ratio = f"{width}:{height}"
        video_info.append([video_file, duration, str(clip.duration), aspect_ratio])

    return video_info


def click():
    print("click")

def get_video_duration(video_path):
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.reader.close()
        return duration

def render_videos(video_path, part_duration, text, output_path):
    black_background = ColorClip((1080, 1920), color=(0, 0, 0), duration=get_video_duration(video_path))

    video = VideoFileClip(video_path)
    video = video.resize(width=black_background.w)
    video = video.set_position('center')
    final_video = CompositeVideoClip([black_background.set_duration(get_video_duration(video_path)), video.set_duration(get_video_duration(video_path))])

    # Split the final video into parts of the specified duration and save them
    start_time = 0
    part_number = 1

    for i in range(1, int(final_video.duration // part_duration) + 1):
        part = final_video.subclip(start_time, min(start_time + part_duration, final_video.duration))
        # Save the current part with text
        text = f"{text} Part {i}"
        text_clip = TextClip(text, fontsize=50, color='white')

        # Set the position of the text
        text_clip = text_clip.set_position('bottom').set_duration(part.duration)

        # Composite the text onto the current part
        part = CompositeVideoClip([part, text_clip])
        part.write_videofile(f"{output_path}/part{i}.mp4", codec="libx264", audio_codec="aac")

        start_time += part_duration



def render_video_thread(video_path, part_duration, output_path, part_number):
    black_background = ColorClip((1080, 1920), color=(0, 0, 0), duration=get_video_duration(video_path))
    margin_left = 50
    margin_right = 50

    video_file_name = os.path.basename(video_path)
    video_file_name = os.path.splitext(video_file_name)[0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video_file_name_directory = os.path.join(output_path, video_file_name)
    if not os.path.exists(video_file_name_directory):
        os.makedirs(video_file_name_directory)

    video = VideoFileClip(video_path)
    video = video.resize(width=black_background.w)
    video = video.set_position('center')
    final_video = CompositeVideoClip([black_background.set_duration(get_video_duration(video_path)), video.set_duration(get_video_duration(video_path))])

    start_time = 0

    for i in range(1, int(final_video.duration // part_duration) + 1):
        part = final_video.subclip(start_time, min(start_time + part_duration, final_video.duration))

        line_width = 30
        wrapped_text = textwrap.fill(video_file_name, width=line_width)
        text_clip_width = 1080 - (margin_left + margin_right)
        title_video = TextClip(wrapped_text, fontsize=50, color='white', size=(text_clip_width, 400))
        x_position = 'center' if margin_left == margin_right else margin_left
        title_video_text_clip = title_video.set_position((x_position, 250)).set_duration(part.duration)

        # Save the current part with text
        part_text = f"Part {part_number}"
        text_clip = TextClip(part_text, fontsize=50, color='white')
        # Set the position of the text
        text_clip = text_clip.set_position(('center', black_background.h - 300)).set_duration(part.duration)

        # Composite the text onto the current part
        part = CompositeVideoClip([part, text_clip, title_video_text_clip])
        video_output_path = video_file_name_directory
        if not os.path.exists(video_output_path):
            os.makedirs(video_output_path)

        # Save the part with the output path and file name
        part.write_videofile(os.path.join(video_output_path, f"{i}.mp4"), codec="libx264", audio_codec="aac")

        start_time += part_duration

def render_videos_multithread(video_paths, part_duration, output_path, num_threads):
    threads = []

    for video_path in video_paths:
        thread = threading.Thread(target=render_video_thread, args=(video_path, part_duration, output_path, len(threads) + 1))
        threads.append(thread)

    # Start and join the threads to process videos concurrently
    for thread in threads[:num_threads]:
        thread.start()

    for thread in threads:
        thread.join()