from flask import Blueprint, request, jsonify
from datetime import datetime
import sqlite3

report_blueprint = Blueprint('notification', __name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@notification_blueprint.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Retrieve user notifications.
    """
    user_email = request.args.get('email')

    if not user_email:
        return jsonify({'message': 'Email is required'}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Luăm notificările utilizatorului și convertim datetime într-un string frumos
        cursor.execute("SELECT id, message, street, datetime FROM notifications WHERE user_email = ?", (user_email,))
        notifications = [
            {"id": row[0], "message": row[1], "street": row[2], "datetime": row[3]} for row in cursor.fetchall()
        ]
        print(notifications)
        conn.close()
        return jsonify(notifications)

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@notification_blueprint.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    user_email = request.json.get('email')  # Obține emailul din corpul cererii

    if not user_email:
        return jsonify({'message': 'Email is required'}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Verificăm dacă notificarea există și dacă aparține utilizatorului
        cursor.execute("SELECT * FROM notifications WHERE id = ? AND user_email = ?", (notification_id, user_email))
        notification = cursor.fetchone()

        if not notification:
            return jsonify({'message': 'Notification not found or does not belong to the user'}), 404

        # Ștergem notificarea
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()

        conn.close()

        # Trimitem un mesaj de succes
        response = jsonify({'message': 'Notification deleted successfully'})
        response.headers["Content-Type"] = "application/json"
        return response, 200

    except Exception as e:
        print(f"Error during delete operation: {str(e)}")  # Înregistrează eroarea pentru debugging
        return jsonify({'message': f'Error: {str(e)}'}), 500