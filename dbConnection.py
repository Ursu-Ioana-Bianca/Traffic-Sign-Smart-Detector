import os
import sqlite3

import folium as folium
from flasgger import Swagger
from flask import Flask, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_restx import Api, Resource

from upload_module import configure_upload_routes, configure_webcam_routes

app = Flask(__name__)
CORS(app)  # 🔥 Permite accesul din alte porturi


app.secret_key = os.urandom(24)
swagger = Swagger(app)
api = Api(app, doc='/documentation')




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




@app.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Register
          required:
            - username
            - email
            - password
            - country
            - county
          properties:
            username:
              type: string
              description: Username-ul utilizatorului
            email:
              type: string
              description: Email-ul utilizatorului
            password:
              type: string
              description: Parola utilizatorului
            country:
              type: string
              description: Țara utilizatorului
            county:
              type: string
              description: Județul utilizatorului
    responses:
      201:
        description: User registered successfully
        schema:
          properties:
            message:
              type: string
              example: "User registered successfully"
      400:
        description: Missing data or duplicate entry
      500:
        description: Unexpected server error
    """
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










from flask import render_template, jsonify, request
from werkzeug.security import check_password_hash
import sqlite3

@app.route('/login', methods=['POST'])
def login():
    """
        User Login
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Login
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: User's email
                password:
                  type: string
                  description: User's password
        responses:
          200:
            description: Successful login
            schema:
              properties:
                message:
                  type: string
                  example: "Login successful"
                username:
                  type: string
                email:
                  type: string
          401:
            description: Invalid credentials
            schema:
              properties:
                message:
                  type: string
                  example: "Invalid credentials"
          400:
            description: Missing data
        """
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Conectare la baza de date
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'message': 'User does not exist'}), 401

        if check_password_hash(user[2], password):
            # Loginul este reușit, redirecționează utilizatorul către user_page
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    # În caz de cerere GET, randează pagina de login
    return render_template('user_page.html')

@app.route('/user_page')
def user_page():
    return render_template('user_page.html')

@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/about')
def help_page():
    return render_template('about.html')


@app.route('/help')
def about_page():
    return render_template('help.html')




from rdflib import OWL, RDF, RDFS, Graph, Namespace

categories = {}
signs_name = []
signs_properties = {}


def load_ontology():
    global categories, signs_name, signs_properties  # Asigură-te că folosești variabilele globale

    # Curățăm datele pentru a preveni dublarea informațiilor
    categories.clear()
    signs_name.clear()
    signs_properties.clear()

    
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
                ?shapeName ?contourColor ?backgroundColor
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

            OPTIONAL {{
                ?sign signs:hasShape ?shape.
                ?shape rdfs:label ?shapeName.

                ?sign signs:hasContourColor ?contour.
                ?contour rdfs:label ?contourColor.

                ?sign signs:hasBackgroundColor ?background.
                ?background rdfs:label ?backgroundColor.
                
            
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

            # Verificăm dacă semnul există deja în listă
            existing_sign = next((s for s in categories[category_name] if s["name"] == str(sign_row.signName)), None)

            if existing_sign:
                # Dacă semnul există deja, verificăm dacă semnul asociat nu este deja adăugat
                if sign_row.associatedSignName is not None:
                    # Verificăm dacă semnul asociat nu există deja în lista de semne asociate
                    associated_sign = next(
                        (s for s in existing_sign["associatedSigns"] if s["name"] == str(sign_row.associatedSignName)),
                        None)

                    if associated_sign is None:
                        # Dacă semnul asociat nu este în lista, îl adăugăm
                        existing_sign["associatedSigns"].append({
                            "name": str(sign_row.associatedSignName),
                            "image": str(
                                sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                        })
            else:
                # Dacă semnul NU există, îl creăm și îl adăugăm în listă
                sign_data = {
                    "name": str(sign_row.signName),
                    "image": str(sign_row.signImageURL),
                    "description": str(sign_row.signDescription),
                    "shape": str(sign_row.shapeName) if sign_row.shapeName is not None else "",
                    "background": str(sign_row.backgroundColor) if sign_row.backgroundColor is not None else "",
                    "contour": str(sign_row.contourColor) if sign_row.contourColor is not None else "",
                    "associatedSigns": []
                }

                if sign_row.associatedSignName is not None:
                    # Verificăm dacă semnul asociat nu există deja
                    associated_sign = {
                        "name": str(sign_row.associatedSignName),
                        "image": str(
                            sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                    }
                    # Verificăm dacă semnul asociat este deja în lista
                    if associated_sign not in sign_data["associatedSigns"]:
                        sign_data["associatedSigns"].append(associated_sign)

                categories[category_name].append(sign_data)  # Adăugăm semnul principal în listă



load_ontology()
configure_upload_routes(app, signs_name, signs_properties)
configure_webcam_routes(app)


@app.route('/get_signs', methods=['GET'])
def get_signs():
    """
    Retrieve Traffic Signs from Ontology
    ---
    tags:
      - Traffic Signs
    responses:
      200:
        description: A list of traffic sign categories and details
        schema:
          type: object
          example:
            {
              "Warning Signs": [
                {
                  "name": "Yield",
                  "image": "http://example.com/yield.png",
                  "description": "Yield to oncoming traffic",
                  "shape": "Triangle",
                  "background": "White",
                  "contour": "Red",
                  "associatedSigns": [
                    {
                      "name": "Stop",
                      "image": "http://example.com/stop.png"
                    }
                  ]
                }
              ]
            }
    """
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
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distanța în km


@app.route('/get_nearby_signs', methods=['GET'])
def get_nearby_signs():
    """
    Retrieve nearby traffic signs based on latitude and longitude.
    ---
    parameters:
      - name: lat
        in: query
        type: number
        required: true
        description: Latitude of the user's location
      - name: lon
        in: query
        type: number
        required: true
        description: Longitude of the user's location
    responses:
      200:
        description: List of nearby traffic signs with details
    """
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


@app.route('/map', methods=['GET'])
def generate_map():
    """
    Generate a map centered on the user's location and display nearby signs.
    ---
    tags:
      - Map
    parameters:
      - name: lat
        in: query
        type: number
        required: true
        description: Latitude of the user's location
      - name: lon
        in: query
        type: number
        required: true
        description: Longitude of the user's location
    responses:
      200:
        description: A map with nearby signs in JSON format
        schema:
          type: object
          properties:
            latitude:
              type: number
              description: Latitude of the center of the map
            longitude:
              type: number
              description: Longitude of the center of the map
            signs:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    description: Name of the sign
                  latitude:
                    type: number
                    description: Latitude of the sign
                  longitude:
                    type: number
                    description: Longitude of the sign
      400:
        description: Missing or invalid parameters
      500:
        description: Server error
    """
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))

    # Create map centered on user location
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], popup="You are here", icon=folium.Icon(color='blue')).add_to(m)

    # Fetch nearby signs
    signs = get_nearby_signs(lat, lon)

    for sign in signs:
        folium.Marker(
            [sign["latitude"], sign["longitude"]],
            popup=sign["name"],
            icon=folium.Icon(color='red')
        ).add_to(m)

    # Return JSON response with nearby signs instead of rendering HTML
    return jsonify({"latitude": lat, "longitude": lon, "signs": signs})


from datetime import datetime


@app.route('/report', methods=['POST'])
def report_issue():
    """
    Submit a new traffic report.
    ---
    parameters:
      - name: description
        in: body
        type: string
        required: true
        description: Description of the traffic issue
      - name: country
        in: body
        type: string
        required: true
        description: Country where the issue occurred
      - name: county
        in: body
        type: string
        required: true
        description: County where the issue occurred
      - name: street
        in: body
        type: string
        required: true
        description: Street where the issue occurred
      - name: datetime
        in: body
        type: string
        format: date-time
        required: true
        description: Date and time of the report (ISO format)
      - name: userEmail
        in: body
        type: string
        required: true
        description: Email of the user reporting the issue
    responses:
      201:
        description: Report submitted successfully
      400:
        description: Missing or invalid data
      500:
        description: Server error
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
        cursor.execute("SELECT email FROM users WHERE country = ? AND county = ? AND email != ?", (country.lower(), county, user_email))

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


@app.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Retrieve user notifications.
    ---
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: Email of the user to fetch notifications for
    responses:
      200:
        description: A list of notifications
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: Notification ID
              message:
                type: string
                description: Notification message
              street:
                type: string
                description: Street where the issue was reported
              datetime:
                type: string
                format: date-time
                description: Date and time of the notification
      400:
        description: Email is required
      500:
        description: Server error
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

        # Trimitem un mesaj de succes
        response = jsonify({'message': 'Notification deleted successfully'})
        response.headers["Content-Type"] = "application/json"
        return response, 200

    except Exception as e:
        print(f"Error during delete operation: {str(e)}")  # Înregistrează eroarea pentru debugging
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    Retrieve user information.
    ---
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: Email of the user
    responses:
      200:
        description: User information retrieved successfully
        schema:
          type: object
          properties:
            username:
              type: string
              description: Username of the user
            email:
              type: string
              description: Email of the user
            country:
              type: string
              description: Country of the user
            county:
              type: string
              description: County of the user
      400:
        description: Email is required
      404:
        description: User not found
      500:
        description: Server error
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







UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    """
    Upload a user profile image.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: profile_image
        in: formData
        type: file
        required: true
        description: The profile image file
      - name: email
        in: formData
        type: string
        required: true
        description: Email of the user
    responses:
      200:
        description: Profile image uploaded successfully
      400:
        description: No file provided or invalid email
      500:
        description: Server error
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


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout the user by clearing the session.
    ---
    responses:
      200:
        description: Logged out successfully
      500:
        description: Server error
    """
    try:
        # Verificăm dacă utilizatorul a facut logout
        if 'userEmail' not in session:
            return jsonify({'message': 'Logged out successfully!'}), 200
        else:
            return jsonify({'message': 'Logged out failed.'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
