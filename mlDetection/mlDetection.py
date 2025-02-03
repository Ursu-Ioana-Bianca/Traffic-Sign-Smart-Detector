# from config import *
import json
import subprocess

import imageio.v3 as iio

from .config import *

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv"]


def ensure_file_exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")


def detect_labels(file_path, path=DARKNET_PATH):
    original_dir = os.getcwd()
    ensure_file_exists(OUTPUT_LABEL_IMAGE)
    ensure_file_exists(OUTPUT_LABEL_VIDEO)
    command, input_type = prepare_command(file_path)
    os.chdir(path)
    subprocess.run(command, shell=True)
    os.chdir(original_dir)
    if input_type == "image":
        path_to_output = os.path.join(DARKNET_PATH, OUTPUT_IMAGE)
        processed_data = extract_label(OUTPUT_LABEL_IMAGE)
    else:
        path_to_output = OUTPUT_VIDEO
        processed_data = extract_label(OUTPUT_LABEL_VIDEO)

    return path_to_output, input_type, processed_data


def prepare_command(file_path):
    input_type = ""
    if file_path == 'webcam':
        command = [
            DARKNET_EXECUTABLE,
            "detector", "demo",
            DATA_FILE,
            CFG_FILE,
            WEIGHTS_FILE,
            "-c", "0"
        ]
        input_type = "webcam"
    else:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in IMAGE_EXTENSIONS:
            command = [
                DARKNET_EXECUTABLE,
                "detector", "test",
                DATA_FILE,
                CFG_FILE,
                WEIGHTS_FILE,
                file_path,
                "-out_filename", OUTPUT_IMAGE,
                "-out", OUTPUT_LABEL_IMAGE,
                "-dont_show"
            ]
            input_type = "image"
        elif file_extension in VIDEO_EXTENSIONS:
            command = [
                DARKNET_EXECUTABLE,
                "detector", "demo",
                DATA_FILE,
                CFG_FILE,
                WEIGHTS_FILE,
                file_path,
                "-out_filename", OUTPUT_VIDEO,
                "-json_file_output", OUTPUT_LABEL_VIDEO,
                "-dont_show"
            ]
            input_type = "video"
        else:
            print("File type not available.")
            command = []

    return command, input_type


def encode_video(source, dest, codec_type="h264"):
    with iio.imopen(dest, "w", plugin="pyav") as out_file:
        out_file.init_video_stream(codec_type, fps=30)

        for frame in iio.imiter(source, plugin="pyav"):
            out_file.write_frame(frame)


def extract_label(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    processed_data = []
    seen_categories = set()

    for entry in data:
        media_path = entry.get('filename', 'default_video_filename.mp4')
        frame_id = entry.get('frame_id', 1)

        for obj in entry['objects']:
            category = obj['name']

            if category not in seen_categories:
                obj_info = {
                    'filename': media_path,
                    'frame_id': frame_id,
                    'class_id': obj['class_id'],
                    'name': category,
                    'relative_coordinates': obj['relative_coordinates'],
                    'confidence': obj['confidence']
                }
                processed_data.append(obj_info)
                seen_categories.add(category)

    return processed_data


if __name__ == "__main__":
    # detect_labels("webcam")
    extract_label(OUTPUT_LABEL_VIDEO)
