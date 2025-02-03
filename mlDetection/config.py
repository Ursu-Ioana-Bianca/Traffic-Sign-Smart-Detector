import os

DARKNET_PATH = r"D:\darknet\darknet\build\darknet\x64"
DARKNET_EXECUTABLE = os.path.join(DARKNET_PATH, "darknet_no_gpu.exe")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(BASE_DIR, 'mlDetection', 'config_files', 'cfg', 'ts_data.data')

BASE_PATH = os.path.join(BASE_DIR, "mlDetection", "config_files")
WEIGHTS_PATH = os.path.join(BASE_PATH, "weights")
CFG_PATH = os.path.join(BASE_PATH, "cfg")
DATA_PATH = os.path.join(BASE_PATH, "data")

WEIGHTS_FILE = ""
CFG_FILE = ""
DATA_FILE = ""

TRAIN_PATH = ""
TEST_PATH = ""
NAMES_PATH = ""

no_classes = 30


def set_model():
    global WEIGHTS_FILE, CFG_FILE, DATA_FILE

    if no_classes == 4:
        WEIGHTS_FILE = os.path.join(WEIGHTS_PATH, "yolov3_ts.weights")
        CFG_FILE = os.path.join(CFG_PATH, "yolov3_ts_test.cfg")
        DATA_FILE = os.path.join(CFG_PATH, "ts_data.data")

    elif no_classes == 30:
        WEIGHTS_FILE = os.path.join(WEIGHTS_PATH, "yolov3_ts_train_german_50000.weights")
        CFG_FILE = os.path.join(CFG_PATH, "yolov3_ts_test_german.cfg")
        DATA_FILE = os.path.join(CFG_PATH, "ts_german_data.data")

    set_data_file()


def set_data_file():
    global TRAIN_PATH, TEST_PATH, NAMES_PATH, DATA_FILE

    common_path = os.path.join(BASE_DIR, "mlDetection", "config_files", "classes", str(no_classes))
    TRAIN_PATH = os.path.join(common_path, "train.txt")
    TEST_PATH = os.path.join(common_path, "test.txt")
    NAMES_PATH = os.path.join(common_path, "classes.names")

    with open(DATA_FILE, 'w') as file:
        file.write(f"classes = 30\n")
        file.write(f"train = {TRAIN_PATH}\n")
        file.write(f"valid = {TEST_PATH}\n")
        file.write(f"names = {NAMES_PATH}\n")
        file.write(f"backup = backup")


set_model()

INPUT_IMAGE = os.path.join(DATA_PATH, 'traffic-sign-to-test.jpg')
OUTPUT_IMAGE = 'predictions.jpg'
INPUT_VIDEO = os.path.join(DATA_PATH, 'test.mp4')
OUTPUT_VIDEO = os.path.join(DATA_PATH, 'test_result.mp4')
OUTPUT_LABEL_IMAGE = os.path.join(DATA_PATH, 'detection_results.json')
OUTPUT_LABEL_VIDEO = os.path.join(DATA_PATH, 'detection_results_video.json')
