import shutil
from flask import request, redirect, url_for, render_template, session, jsonify
from werkzeug.utils import secure_filename
import os
from rapidfuzz import process
import subprocess

from mlDetection import mlDetection


def configure_upload_routes(app, signs_name, signs_properties):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    STATIC_FOLDER = os.path.join(os.getcwd(), 'static', 'processed_uploads')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                filepath = filepath.replace("\\", "/")
                file.save(filepath)

                result_path, input_type, processed_data = mlDetection.detect_labels(filepath)
                if result_path and os.path.exists(result_path):
                    if input_type == 'video':
                        encoded_file_path = os.path.join(UPLOAD_FOLDER,
                                                         'encoded_' + os.path.basename(result_path))
                        mlDetection.encode_video(result_path, encoded_file_path)
                    elif input_type == 'image':
                        encoded_file_path = result_path

                    if os.path.exists(encoded_file_path):
                        static_path = os.path.join(STATIC_FOLDER, os.path.basename(encoded_file_path))
                        shutil.move(encoded_file_path, static_path)
                        file_url = url_for('static', filename='processed_uploads/' + os.path.basename(static_path))
                        session['file_url'] = file_url
                        session['input_type'] = input_type

                        detected_objects = []
                        for element in processed_data:
                            detected_objects.append(element['name'])

                        session['detected_objects'] = detected_objects

                        return redirect(url_for('display_results'))
                    else:
                        print("Encoding failed or file does not exist post-encoding.")
                else:
                    print(f"Error: {result_path} does not exist.")
        return render_template('index.html')

    @app.route('/display')
    def display_results():
        file_url = session.get('file_url', None)
        input_type = session.get('input_type', None)
        detected_objects = session.get('detected_objects', None)
        signs_description = handle_processed_data(detected_objects, signs_name, signs_properties)
        return render_template('display_results.html', file_url=file_url, input_type=input_type,
                               detected_objects=detected_objects, signs_description=signs_description)


def configure_webcam_routes(app):
    @app.route('/start_webcam', methods=['GET', 'POST'])
    def start_webcam():
        mlDetection.detect_labels("webcam")
        # global darknet_process
        # if darknet_process is None or darknet_process.poll() is not None:
        #     # Only start a new process if there isn't one already running
        #     command = [
        #         mlDetection.DARKNET_EXECUTABLE,
        #         "detector", "demo",
        #         mlDetection.DATA_FILE,
        #         mlDetection.CFG_FILE,
        #         mlDetection.WEIGHTS_FILE,
        #         "-c", "0"
        #     ]
        #     darknet_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     print("Started new webcam process.")
        # else:
        #     print("Webcam process is already running.")

    @app.route('/stop_webcam', methods=['GET', 'POST'])
    def stop_webcam():
        # if mlDetection.darknet_process is not None and mlDetection.darknet_process.poll() is None:
        #     mlDetection.darknet_process.terminate()
        #     mlDetection.darknet_process = None  # Reset the global variable after stopping the process
        #     return jsonify({'message': 'Webcam stopped successfully'}), 200
        # return jsonify({'message': 'Webcam is not running'}), 404
        global darknet_process
        if darknet_process is not None:
            if darknet_process.poll() is None:
                darknet_process.terminate()
                print("Stopped the webcam process.")
            else:
                print("Webcam process was not running.")
        else:
            print("No webcam process to stop.")


def handle_processed_data(processed_data, signs_name, signs_properties):
    signs_description = []
    for element in processed_data:
        sign_name = element
        best_match = process.extractOne(sign_name, signs_name)
        print(best_match)
        if best_match:
            sign_name = best_match[0]
            print(signs_properties[sign_name][0].get('image')
                  )
            sign_image = signs_properties[sign_name][0].get('image')
            sign_description = signs_properties[sign_name][0].get('description')
            sign_category = signs_properties[sign_name][0].get('category')

        signs_description.append({
            "name": sign_name,
            "image": sign_image,
            "description": f"Description: {sign_description}",
            "category": f"Category: {sign_category}"
        })

    return signs_description
