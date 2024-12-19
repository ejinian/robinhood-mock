from flask import Flask
from flask_cors import CORS
from app.routes import api_blueprint
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app, supports_credentials=True)
    app.config['SECRET_KEY'] = 'not_a_real_key'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
    app.config['SESSION_COOKIE_PATH'] = '/'
    app.register_blueprint(api_blueprint)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
