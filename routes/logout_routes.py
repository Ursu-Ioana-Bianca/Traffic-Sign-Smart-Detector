import os
import sqlite3
from flask import Blueprint, request, jsonify

user_blueprint = Blueprint('logout', __name__)

UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@logout_blueprint.route('/logout', methods=['POST'])
def logout():
    """
    Logout the user by clearing the session.
    """
    try:
        # Verificăm dacă utilizatorul a facut logout
        if 'userEmail' not in session:
            return jsonify({'message': 'Logged out successfully!'}), 200
        else:
            return jsonify({'message': 'Logged out failed.'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500