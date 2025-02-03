from flask import Blueprint, request, jsonify, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        country = data.get('country')
        county = data.get('county')

        if not username or not email or not password or not country or not county:
            return jsonify({'message': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, password, country, county) VALUES (?, ?, ?, ?, ?)",
                       (username, email, hashed_password, country, county))

        conn.commit()

        # Verifică existența rapoartelor
        cursor.execute("SELECT description, datetime, street FROM reports WHERE country = ? AND county = ?",
                       (country.capitalize(), county))
        reports = cursor.fetchall()

        # Dacă există rapoarte, adaugă notificări pentru utilizator
        if reports:
            for report in reports:
                report_description, report_datetime, report_street = report
                cursor.execute("INSERT INTO notifications (user_email, message, street, datetime) VALUES (?, ?, ?, ?)",
                               (email,
                                f"New issue: {report_description}<br>Reported in your area: {report_street}<br>Reported at: {report_datetime}",
                                report_street, report_datetime))

        conn.commit()
        conn.close()

        return jsonify({'message': 'User registered successfully'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400
    except Exception as e:
        return jsonify({'message': f"Unexpected error: {e}"}), 500
