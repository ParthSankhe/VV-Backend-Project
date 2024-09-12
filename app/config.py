# Configuration (e.g. size, duration limits, database URL)
import os

print("Loading config.py")


class Config:
    MAX_VIDEO_SIZE_MB = 50  
    MIN_VIDEO_DURATION_SECS = 3
    MAX_VIDEO_DURATION_SECS = 30
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TOKEN = os.getenv("API_TOKEN", "hardcoded_token_12345")  
    BASE_URL = 'http://localhost:5000'
