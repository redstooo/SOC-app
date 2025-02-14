import os
import threading
import requests
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from db import db
from resources.chemical import blp as ChemicalBlueprint
from resources.reaction import blp as ReactionBlueprint

# Import Kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from flask_migrate import Migrate

def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

    # Register API Blueprints
    api.register_blueprint(ChemicalBlueprint)
    api.register_blueprint(ReactionBlueprint)

    return app

# Function to run Flask in a separate thread
def run_flask():
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

# Kivy GUI
class MyKivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Button to fetch chemical data
        self.chemical_button = Button(text="Get Chemical Data", font_size=20)
        self.chemical_button.bind(on_press=self.get_chemical_data)

        # Button to fetch reaction data
        self.reaction_button = Button(text="Get Reaction Data", font_size=20)
        self.reaction_button.bind(on_press=self.get_reaction_data)

        # Add buttons to layout
        layout.add_widget(self.chemical_button)
        layout.add_widget(self.reaction_button)

        return layout

    def get_chemical_data(self, instance):
        try:
            response = requests.get("http://127.0.0.1:5000/chemical")
            if response.status_code == 200:
                self.chemical_button.text = response.json().get("message", "Chemical data retrieved")
            else:
                self.chemical_button.text = "Error: " + str(response.status_code)
        except requests.exceptions.RequestException:
            self.chemical_button.text = "Flask not running!"

    def get_reaction_data(self, instance):
        try:
            response = requests.get("http://127.0.0.1:5000/get_all_reactions")
            if response.status_code == 200:
                self.reaction_button.text = response.json().get("message", "Reaction data retrieved")
            else:
                self.reaction_button.text = "Error: " + str(response.status_code)
        except requests.exceptions.RequestException:
            self.reaction_button.text = "Flask not running!"

if __name__ == "__main__":
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start Kivy GUI
    MyKivyApp().run()