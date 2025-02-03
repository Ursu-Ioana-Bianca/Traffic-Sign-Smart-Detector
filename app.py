from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_restx import Api

from database.db import create_db
from routes.auth_routes import auth_blueprint
from routes.page_routes import page_blueprint
from routes.ontology_routes import ontology_blueprint
from routes.logout_routes import logout_blueprint
from routes.notification_routes import notification_blueprint
from routes.signs_routes import signs_blueprint
from routes.map_routes import map_blueprint
from routes.report_routes import report_blueprint
from routes.user_routes import user_blueprint

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
app.secret_key = "your_secret_key"

swagger = Swagger(app)
api = Api(app, doc='/documentation')

# Create database tables if they don’t exist
create_db()

# Register blueprints (modularized routes)
app.register_blueprint(auth_blueprint)
app.register_blueprint(page_blueprint)
app.register_blueprint(ontology_blueprint)
app.register_blueprint(logout_blueprint)

# Încărcăm ontologia o singură dată la pornirea aplicației
load_ontology()

# Înregistrăm rutele din fișierele separate
app.register_blueprint(signs_blueprint)
app.register_blueprint(map_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(notification_blueprint)
app.register_blueprint(logout_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
