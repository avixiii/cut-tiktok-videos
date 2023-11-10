import os
import threading
from tkinter import Tk, Label, Button, Entry, filedialog

from app.utils import render_videos_multithread


class VideoProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Processor")

        self.label_folder = Label(master, text="Enter folder:")
        self.label_folder.grid(row=0, column=0)

        self.entry_folder = Entry(master)
        self.entry_folder.grid(row=0, column=1)

        self.button_browse = Button(master, text="Browse", command=self.browse_folder)
        self.button_browse.grid(row=0, column=2)

        self.label_output_folder = Label(master, text="Enter output folder:")
        self.label_output_folder.grid(row=1, column=0)

        self.entry_output_folder = Entry(master)
        self.entry_output_folder.grid(row=1, column=1)

        self.button_browse_output = Button(master, text="Browse", command=self.browse_output_folder)
        self.button_browse_output.grid(row=1, column=2)

        self.label_num_threads = Label(master, text="Enter num threads:")
        self.label_num_threads.grid(row=2, column=0)

        self.entry_num_threads = Entry(master)
        self.entry_num_threads.grid(row=2, column=1)

        self.label_part_duration = Label(master, text="Enter time/video:")
        self.label_part_duration.grid(row=3, column=0)

        self.entry_part_duration = Entry(master)
        self.entry_part_duration.grid(row=3, column=1)

        self.button_process = Button(master, text="Process Videos", command=self.process_videos)
        self.button_process.grid(row=4, column=0, columnspan=3)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.entry_folder.delete(0, "end")
        self.entry_folder.insert(0, folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.entry_output_folder.delete(0, "end")
        self.entry_output_folder.insert(0, folder_path)

    def process_videos(self):
        input_folder = self.entry_folder.get()
        output_folder = self.entry_output_folder.get()
        num_threads = int(self.entry_num_threads.get())
        part_duration = int(self.entry_part_duration.get())

        video_paths = [os.path.join(input_folder, video_file) for video_file in os.listdir(input_folder) if
                       video_file.endswith((".mp4", ".avi"))]

        render_videos_multithread(video_paths, part_duration, output_folder, num_threads)


if __name__ == "__main__":
    root = Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
