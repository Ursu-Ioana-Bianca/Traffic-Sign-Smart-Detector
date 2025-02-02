import os
import sqlite3

from flask import Flask, jsonify, request, session
from flask_cors import CORS  # ✅ Importă CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Permite cookie-urile de sesiune
# CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.urandom(24)



def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Creare tabel utilizatori
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      country TEXT,
                      county TEXT,
                      profile_image TEXT)
                   ''')

    # Creare tabel notificări
    cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_email TEXT NOT NULL,
                      message TEXT NOT NULL,
                      seen INTEGER DEFAULT 0,  -- 0 = nevăzut, 1 = văzut
                      street TEXT NOT NULL,
                      datetime DATETIME,
                      FOREIGN KEY (user_email) REFERENCES users(email))
                   ''')

    # ✅ Adaugă tabelul pentru rapoarte
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      description TEXT NOT NULL,
                      country TEXT NOT NULL,
                      county TEXT NOT NULL,
                      street TEXT NOT NULL,
                      datetime DATETIME)
                   ''')

    conn.commit()
    conn.close()

create_db()

from datetime import datetime


@app.route('/register', methods=['POST'])
def register():
    try:
        print("Request received at /register")  # 📌 Debugging
        data = request.json
        print("Received data:", data)  # 📌 Verificăm ce primim de la frontend

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        country = data.get('country')
        county = data.get('county')
        

        if not username or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # ✅ Inserăm utilizatorul în baza de date (acum și cu strada)
        cursor.execute("INSERT INTO users (username, email, password, country, county) VALUES (?, ?, ?, ?, ?)",
                       (username, email, hashed_password, country.lower(), county))
        
        conn.commit()

        print(country.capitalize())
        print(county)
        # ✅ Verificăm dacă există rapoarte pentru țara, județul și strada utilizatorului
        cursor.execute("SELECT description, datetime, street FROM reports WHERE country = ? AND county = ?",
                       (country.capitalize(), county))
        reports = cursor.fetchall()
        print(reports)
        # ✅ Dacă există rapoarte, adăugăm notificări pentru utilizator
        if reports:
            for report in reports:
                report_description = report[0]
                report_datetime = report[1]  # Data raportului existent
                report_street = report[2]  # Strada raportului
                cursor.execute("INSERT INTO notifications (user_email, message, street, datetime) VALUES (?, ?, ?, ?)",
                               (email, f"New issue: {report_description}<br>Reported in your area: {report_street}<br>Reported at: {report_datetime}", report_street, report_datetime))

        conn.commit()
        conn.close()

        print("User registered successfully!")  # 📌 Verificăm dacă ajunge aici
        return jsonify({'message': 'User registered successfully'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")  # 📌 Debugging pentru orice eroare
        return jsonify({'message': f"Unexpected error: {e}"}), 500
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'message': 'User does not exist'}), 200

    if check_password_hash(user[2], password):
        return jsonify({'message': 'Login successful', 'username': user[1], 'email': email}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401



    
from rdflib import OWL, RDF, RDFS, Graph, Namespace

categories = {}
signs_name = []
signs_properties = {}

def load_ontology():
    g = Graph()
    g.parse("TrafficSignOntology.rdf", format="xml")  # Poate fi "turtle", "n3", "nt" în funcție de format
        # Execută interogarea pentru a obține toate categoriile
    category_query = """
    PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?signCategoryName
    WHERE {
        ?sign signs:category ?signCategory.
        ?signCategory rdfs:label ?signCategoryName.
    }
    ORDER BY ?signCategoryName
"""
    category_results = g.query(category_query)

    

    for category_row in category_results:
        category_name = str(category_row.signCategoryName)
        categories[category_name] = []

        sign_query = f"""
        PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?signName ?signImageURL ?signDescription ?associatedSignName ?associatedSignImageUrl
        WHERE {{
            ?sign signs:signName ?signName. 
            ?sign signs:signImageURL ?signImageURL.
            ?sign signs:description ?signDescription.
            ?sign signs:category ?signCategory.
            ?signCategory rdfs:label ?signCategoryName.

            OPTIONAL {{
                ?sign signs:hasAssociatedSign ?associatedSign.
                ?associatedSign rdfs:label ?associatedSignName.
                ?associatedSign signs:signImageURL ?associatedSignImageUrl.
            }}
           
            FILTER (STR(?signCategoryName) = "{category_name}")
        }}
        ORDER BY ?signName
        """
        
        sign_results = g.query(sign_query)
        
        for sign_row in sign_results:
            signs_name.append(str(sign_row.signName))

           
            signs_properties[str(sign_row.signName)] = []
            signs_properties[str(sign_row.signName)].append({
                "image": str(sign_row.signImageURL),
                "description": str(sign_row.signDescription),
                "category": category_name,                  
                })
            # categories[category_name].append({
            #     "name": str(sign_row.signName),
            #     "image": str(sign_row.signImageURL),
            #     "description": str(sign_row.signDescription)
            # })

            # Verificăm dacă semnul există deja în listă
            existing_sign = next((s for s in categories[category_name] if s["name"] == str(sign_row.signName)), None)

            if existing_sign:
                # Dacă semnul există deja, adăugăm doar semnul asociat
                if sign_row.associatedSignName is not None:
                    existing_sign["associatedSigns"].append({
                        "name": str(sign_row.associatedSignName),
                        "image": str(sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                    })
            else:
                # Dacă semnul NU există, îl creăm și îl adăugăm în listă
                sign_data = {
                    "name": str(sign_row.signName),
                    "image": str(sign_row.signImageURL),
                    "description": str(sign_row.signDescription),
                    "associatedSigns": []
                }

                if sign_row.associatedSignName is not None:
                    sign_data["associatedSigns"].append({
                        "name": str(sign_row.associatedSignName),
                        "image": str(sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                    })

                categories[category_name].append(sign_data)  # Adăugăm semnul principal în listă

@app.route('/get_signs', methods=['GET'])
def get_signs():

    load_ontology()
    return jsonify(categories)




import math

import requests
from rapidfuzz import process


# Funcție pentru calculul distanței dintre două puncte GPS (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Raza Pământului în km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Distanța în km

@app.route('/get_nearby_signs', methods=['GET'])
def get_nearby_signs():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # Interogare Overpass API pentru a găsi semne de circulație în apropiere
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
        node["traffic_sign"](around:50000,{lat},{lon});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()


    nearby_signs = []
    for element in data.get("elements", []):
        if "tags" in element:
            sign_name = element["tags"].get("traffic_sign", "Unknown Sign")
            sign_lat = element["lat"]
            sign_lon = element["lon"]
            distance = haversine(float(lat), float(lon), sign_lat, sign_lon)

            load_ontology()
            # Găsim cel mai apropiat nume din 'signs_name' folosind rapidfuzz
            best_match = process.extractOne(sign_name, signs_name)
            if best_match:
                sign_name = best_match[0]
                print(signs_properties[sign_name][0].get('image')
 )
                sign_image = signs_properties[sign_name][0].get('image')
                sign_description = signs_properties[sign_name][0].get('description')
                sign_category = signs_properties[sign_name][0].get('category')
 
            nearby_signs.append({
                "name": sign_name,
                "latitude": sign_lat,
                "longitude": sign_lon,
                "distance": round(distance, 2),
                "image": sign_image,
                "description": f"Description: {sign_description}",
                "category": f"Category: {sign_category}"
            })


    return jsonify(nearby_signs)






from datetime import datetime


@app.route('/report', methods=['POST'])
def report_issue():
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
        cursor.execute("SELECT email FROM users WHERE country = ? AND county = ? AND email != ?", (country.lower(), county, user_email))
        users = cursor.fetchall()
 
        # Adăugăm notificări pentru fiecare utilizator
        for user in users:
                cursor.execute("INSERT INTO notifications (user_email, message, street, datetime) VALUES (?, ?, ?, ?)",
                            (user[0], f"New issue: {issue_description}<br>Reported in your area: {street}<br>Raported at: {datetime_obj} ", street, datetime_obj))
        print(users[0])
        conn.commit()
        conn.close()

        return jsonify({'message': 'Report submitted successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    

@app.route('/notifications', methods=['GET'])
def get_notifications():
    user_email = request.args.get('email')
    #user_email = session.get('userEmail')  # Ia emailul din sesiune

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



@app.route('/get_user_info', methods=['GET'])
def get_user_info():
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
    
@app.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
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

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
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



    
    
@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Verificăm dacă utilizatorul a facut logout
        if 'userEmail' not in session:
            return jsonify({'message': 'Logged out successfully!'}), 200
        else:
            return jsonify({'message': 'Logged out failed.'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500  
    


if __name__ == '__main__':
    app.run(debug=True)  # ✅ Specifică portul
