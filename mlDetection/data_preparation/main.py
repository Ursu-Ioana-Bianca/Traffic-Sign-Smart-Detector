import os
import pandas as pd
import cv2

BASE_PATH = r"C:\irina\prepare_gtsrb\Traffic-Signs-Data-German"
train_csv_path = os.path.join(BASE_PATH, "Train.csv")
test_csv_path = os.path.join(BASE_PATH, "Test.csv")
output_folder = os.path.join(BASE_PATH, "filtered_dataset")

filtered_train_folder = os.path.join(output_folder, "train")
filtered_test_folder = os.path.join(output_folder, "test")
os.makedirs(filtered_train_folder, exist_ok=True)
os.makedirs(filtered_test_folder, exist_ok=True)

train_df = pd.read_csv(train_csv_path)
test_df = pd.read_csv(test_csv_path)

excluded_classes = {42, 22, 25, 16, 10, 8, 0, 38, 39, 24, 26, 29, 30}
train_df = train_df[~train_df["ClassId"].isin(excluded_classes)]
test_df = test_df[~test_df["ClassId"].isin(excluded_classes)]

filtered_train_df = train_df.groupby("ClassId").apply(
    lambda x: x.sample(n=min(225, len(x)), random_state=42)).reset_index(drop=True)
filtered_test_df = test_df.groupby("ClassId").apply(
    lambda x: x.sample(n=min(25, len(x)), random_state=42)).reset_index(drop=True)


def process_images_and_annotations(df, source_folder, output_folder):
    for _, row in df.iterrows():
        class_id = str(row["ClassId"])
        img_path = row["Path"]
        src_path = os.path.join(source_folder, img_path)

        if not os.path.exists(src_path):
            continue

        img = cv2.imread(src_path)
        if img is None:
            continue

        class_folder = os.path.join(output_folder, class_id)
        os.makedirs(class_folder, exist_ok=True)
        new_filename = os.path.splitext(os.path.basename(img_path))[0] + '.jpg'
        output_img_path = os.path.join(class_folder, new_filename)
        cv2.imwrite(output_img_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        width, height = img.shape[1], img.shape[0]
        x1, y1, x2, y2 = row['Roi.X1'], row['Roi.Y1'], row['Roi.X2'], row['Roi.Y2']
        x_center = (x1 + x2) / 2.0 / width
        y_center = (y1 + y2) / 2.0 / height
        box_width = (x2 - x1) / width
        box_height = (y2 - y1) / height
        yolo_format = f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"

        yolo_txt_path = output_img_path.replace('.jpg', '.txt')
        with open(yolo_txt_path, "w") as file:
            file.write(yolo_format + "\n")


def generate_path_files():
    train_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(filtered_train_folder) for f in filenames if f.endswith('.jpg')]
    test_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(filtered_test_folder) for f in filenames if f.endswith('.jpg')]

    with open(os.path.join(output_folder, "train.txt"), "w") as file:
        file.writelines(f"{path}\n" for path in train_paths)

    with open(os.path.join(output_folder, "test.txt"), "w") as file:
        file.writelines(f"{path}\n" for path in test_paths)


process_images_and_annotations(filtered_train_df, BASE_PATH, filtered_train_folder)
process_images_and_annotations(filtered_test_df, BASE_PATH, filtered_test_folder)

generate_path_files()


print("Dataset processing and annotation conversion complete. Data is ready for YOLO training.")
