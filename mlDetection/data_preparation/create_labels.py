import os
import cv2

BASE_PATH = r"C:\irina\prepare_gtsrb\Traffic-Signs-Data-German\\"
dataset_folder = os.path.join(BASE_PATH, "filtered_dataset")
train_folder = os.path.join(BASE_PATH, os.path.join(dataset_folder, "train"))
test_folder = os.path.join(BASE_PATH, os.path.join(dataset_folder, "test"))
annotations_train = os.path.join(BASE_PATH, "train_annotation.txt")  # Adjust this if needed
annotations_test = os.path.join(BASE_PATH, "test_annotation.txt")
output_train = os.path.join(BASE_PATH, os.path.join(dataset_folder, "yolo_train"))
output_test = os.path.join(BASE_PATH, os.path.join(dataset_folder, "yolo_test"))

os.makedirs(dataset_folder, exist_ok=True)

excluded_classes = {42, 22, 25, 16, 10, 8, 0, 38, 39, 24, 26, 29, 30}


def convert_to_yolo_format(width, height, x1, y1, x2, y2):
    x_center = (x1 + x2) / 2.0 / width
    y_center = (y1 + y2) / 2.0 / height
    box_width = (x2 - x1) / width
    box_height = (y2 - y1) / height
    return f"{x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"


def process_annotations(annotation_txt, image_folder, output_folder):
    with open(annotation_txt, "r") as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) < 8 or int(parts[7]) in excluded_classes:
                continue

            filename, width, height, x1, y1, x2, y2, class_id = parts[:8]
            width, height, x1, y1, x2, y2, class_id = map(int, [width, height, x1, y1, x2, y2, class_id])

            src_path = os.path.join(image_folder, filename)
            if not os.path.exists(src_path):
                continue

            img = cv2.imread(src_path)
            if img is None:
                continue

            class_folder = os.path.join(output_folder, str(class_id))
            os.makedirs(class_folder, exist_ok=True)

            new_filename = filename.replace(".png", ".jpg")
            output_img_path = os.path.join(class_folder, new_filename)
            cv2.imwrite(output_img_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            yolo_annotation = convert_to_yolo_format(width, height, x1, y1, x2, y2)
            yolo_txt_path = output_img_path.replace(".jpg", ".txt")
            with open(yolo_txt_path, "w") as yolo_file:
                yolo_file.write(f"{class_id} {yolo_annotation}\n")


process_annotations(annotations_train, train_folder, os.path.join(dataset_folder, "yolo_train"))
process_annotations(annotations_test, test_folder, os.path.join(dataset_folder, "yolo_test"))

print("Annotation processing complete. Dataset is ready for YOLO.")
