from flask import Blueprint, request, jsonify
from datetime import datetime
import sqlite3

report_blueprint = Blueprint('report', __name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@report_blueprint.route('/report', methods=['POST'])
def report_issue():
    """
    Submit a new traffic report.
    """
    data = request.json
    issue_description = data.get('description')
    country = data.get('country')
    county = data.get('county')
    street = data.get('street')
    datetime_str = data.get('datetime')
    user_email = data.get('userEmail')

    if not issue_description or not country or not county or not street or not datetime_str:
        return jsonify({'message': 'All fields are required'}), 400

    try:
        # Convertim string-ul datetime la format Python
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Salvăm raportul cu data în format DATETIME
        cursor.execute("INSERT INTO reports (description, country, county, street, datetime) VALUES (?, ?, ?, ?, ?)",
                       (issue_description, country, county, street, datetime_obj))
        conn.commit()

        # Găsim utilizatorii afectați
        cursor.execute("SELECT email FROM users WHERE country = ? AND county = ? AND email != ?",
                       (country.lower(), county, user_email))

        users = cursor.fetchall()

        # Adăugăm notificări pentru fiecare utilizator
        if users:
            for user in users:
                cursor.execute("INSERT INTO notifications (user_email, message, street, datetime) VALUES (?, ?, ?, ?)",
                               (user[0],
                                f"New issue: {issue_description}<br>Reported in your area: {street}<br>Raported at: {datetime_obj} ",
                                street, datetime_obj))
            print(users[0])
            conn.commit()
        conn.close()

        return jsonify({'message': 'Report submitted successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500





