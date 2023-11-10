from app.utils import *

if __name__ == "__main__":
    # input_folder = "/Users/avixiii/Desktop/videos/"
    # output_folder = "/Users/avixiii/Desktop/outputs"
    # num_threads = 2  # Set the number of threads
    input_folder = input("enter folder: ")
    output_folder = input("enter folder output: ")
    num_threads = int(input("enter num threads: "))
    part_duration = int(input("enter time/video: "))

    video_paths = [os.path.join(input_folder, video_file) for video_file in os.listdir(input_folder) if
                   video_file.endswith((".mp4", ".avi"))]

    render_videos_multithread(video_paths, part_duration, output_folder, num_threads)
