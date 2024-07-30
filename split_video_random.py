import os
import random
import subprocess

def get_first_four_chars(input_str):
    return input_str[:4]

# 拆分视频 随机拆分视频
def split_video(input_file, output_dir, min_duration=2, max_duration=5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    prefix = get_first_four_chars(input_file)
    print(f"prefix = {prefix}")

    input_file = os.path.abspath(input_file)
    output_dir = os.path.abspath(output_dir)

    # Get video duration
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result)
    duration = float(result.stdout.decode())

    # Calculate the number of segments and their durations
    num_segments = int(duration // (max(min_duration, max_duration) / 2))
    segment_durations = [random.uniform(min_duration, max_duration) for _ in range(num_segments)]
    remaining_duration = duration - sum(segment_durations)
    segment_durations[-1] += remaining_duration

    # Split the video
    for i, duration in enumerate(segment_durations):
        start_time = sum(segment_durations[:i])
        output_file = os.path.join(output_dir, f"{prefix}_segment_{i:03}.mp4")
#         command = f"ffmpeg -i '{input_file}' -ss {start_time} -t {duration} -c copy '{output_file}'"
# 使用 -avoid_negative_ts make_zero 选项：这种方法可能会导致输出视频在拆分点之前开始，但可以让所有播放器正确播放这些文件。
        command = f"ffmpeg -ss {start_time} -i '{input_file}' -t {duration} -c copy -avoid_negative_ts make_zero '{output_file}'"
        subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    input_file = "raw_data/tts.mp4"
    output_dir = "filelists/main"
    split_video(input_file, output_dir)
