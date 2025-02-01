# Set paths to darknet folders

import os

DARKNET_PATH = r"D:\Code\darknet\darknet\build\darknet\x64"
DARKNET_EXECUTABLE = os.path.join(DARKNET_PATH, "darknet_no_gpu.exe")

BASE_PATH = r"D:/Code/darknet/darknet/"
BASE_PATH_WEIGHTS = r"weights/"
BASE_PATH_CFG = r"cfg/"
BASE_PATH_DATA = r"data/"

WEIGHTS_FILE = os.path.join(BASE_PATH, BASE_PATH_WEIGHTS, "yolov3_ts.weights")
CFG_FILE = os.path.join(BASE_PATH, BASE_PATH_CFG, "yolov3_ts_test.cfg")
DATA_FILE = os.path.join(BASE_PATH, BASE_PATH_CFG, "ts_data.data")

INPUT_IMAGE = os.path.join(BASE_PATH, BASE_PATH_DATA, 'traffic-sign-to-test.jpg')
OUTPUT_IMAGE = 'predictions.jpg'

INPUT_VIDEO = os.path.join(BASE_PATH, BASE_PATH_DATA, 'test.mp4')
OUTPUT_VIDEO = os.path.join(BASE_PATH, BASE_PATH_DATA, 'test_result.mp4')

OUTPUT_LABEL_IMAGE = os.path.join(BASE_PATH, BASE_PATH_DATA, 'detection_results.json')
OUTPUT_LABEL_VIDEO = os.path.join(BASE_PATH, BASE_PATH_DATA, 'detection_results_video.json')
