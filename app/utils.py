import os

from PyQt5.QtWidgets import QFileDialog, QTableWidget
from moviepy.editor import VideoFileClip


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
