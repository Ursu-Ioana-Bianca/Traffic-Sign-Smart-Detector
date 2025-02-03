import os
import sqlite3
from flask import Blueprint, request, jsonify

user_blueprint = Blueprint('user', __name__)

UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@user_blueprint.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    Retrieve user information.
    """
    email = request.args.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT username, email, country, county FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'username': user[0],
            'email': user[1],
            'country': user[2],
            'county': user[3],

        })

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@user_blueprint.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    """
    Upload a user profile image.
    """
    if 'profile_image' not in request.files:  # Folosim 'profile_image' ca cheia corectă
        return jsonify({'message': 'No file provided'}), 400

    file = request.files['profile_image']  # Accesăm fișierul cu cheia corectă
    user_email = request.form.get('email')

    if not user_email:
        return jsonify({'message': 'Email is required'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename).replace("\\", "/")  # Construim calea fișierului

    # Salvăm fișierul pe server
    file.save(file_path)

    # Actualizăm în baza de date cu calea fișierului
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET profile_image = ? WHERE email = ?", (file_path, user_email))
    conn.commit()
    conn.close()

    image_url = f"http://127.0.0.1:5000/static/uploads/{file.filename}"
    return jsonify({'message': 'Profile image updated successfully!', 'image_url': image_url}), 200


