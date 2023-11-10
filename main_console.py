from app.utils import *

if __name__ == "__main__":
    input_folder = "/Users/avixiii/Desktop/videos/"
    output_folder = "/Users/avixiii/Desktop/outputs"
    part_duration = 5
    num_threads = 2  # Set the number of threads
    video_paths = [os.path.join(input_folder, video_file) for video_file in os.listdir(input_folder) if video_file.endswith((".mp4", ".avi"))]

    print(video_paths)

    render_videos_multithread(video_paths, part_duration, output_folder, num_threads)