# Initializes the Flask app
from flask import Flask
from app.config import Config
from app.models import db

print("Loading __init__.py")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes import video_bp
    app.register_blueprint(video_bp)

    return app
