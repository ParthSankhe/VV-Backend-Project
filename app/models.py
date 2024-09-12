# Defines the Video model for SQLite
from flask_sqlalchemy import SQLAlchemy

print("Loading models.py")

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    file_size = db.Column(db.Float, nullable=False)  #in MB
    duration = db.Column(db.Float, nullable=False)    #in seconds
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
