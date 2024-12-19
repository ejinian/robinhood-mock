from flask import Flask
from flask_cors import CORS
from app.routes import api_blueprint
from .models import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    app.register_blueprint(api_blueprint)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
