import shutil
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
import os

from mlDetection import mlDetection

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['STATIC_FOLDER'] = os.path.join(os.getcwd(), 'static', 'processed_uploads')
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath = filepath.replace("\\", "/")
            file.save(filepath)

            result_path, input_type, processed_data = mlDetection.detect_labels(filepath)

            if result_path and os.path.exists(result_path):
                if input_type == 'video':
                    encoded_file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                                     'encoded_' + os.path.basename(result_path))
                    mlDetection.encode_video(result_path, encoded_file_path)
                elif input_type == 'image':
                    encoded_file_path = result_path

                if os.path.exists(encoded_file_path):
                    static_path = os.path.join(app.config['STATIC_FOLDER'], os.path.basename(encoded_file_path))
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
    return render_template('display_results.html', file_url=file_url, input_type=input_type, detected_objects=detected_objects)


if __name__ == '__main__':
    app.run(debug=True)
