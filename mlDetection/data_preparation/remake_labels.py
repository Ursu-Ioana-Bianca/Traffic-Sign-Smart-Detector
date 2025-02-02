import os

base_path = r"../config_files"
train_folder = os.path.join(base_path, "train")
test_folder = os.path.join(base_path, "test")

existing_classes = sorted(set(range(43)) - {42, 22, 25, 16, 10, 8, 0, 38, 39, 24, 26, 29, 30})

class_mapping = {old_id: new_id for new_id, old_id in enumerate(existing_classes)}
print("Class ID Mapping:", class_mapping)


def update_class_ids(folder):
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(subdir, file)

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                if lines:
                    parts = lines[0].strip().split()
                    old_class_id = int(parts[0])
                    if old_class_id in class_mapping:
                        new_class_id = class_mapping[old_class_id]
                        new_line = f"{new_class_id} " + " ".join(parts[1:]) + "\n"

                        with open(file_path, 'w') as f:
                            f.write(new_line)


update_class_ids(train_folder)
update_class_ids(test_folder)

print("Annotation class IDs have been updated based on new mapping.")
