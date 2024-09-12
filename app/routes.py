# API routes for uploading, trimming, merging videos
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.models import db, Video
from app.config import Config
from app.utils import allowed_file, save_video_file, get_video_duration, trim_video_file

video_bp = Blueprint('video_bp', __name__)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    token = request.headers.get('Authorization')
    if token != "Bearer " + Config.API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400
    
    video = request.files['video']
    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video_path = save_video_file(video, filename)

        file_size = os.path.getsize(video_path) / (1024 * 1024)  # in MB
        if file_size > Config.MAX_VIDEO_SIZE_MB:
            return jsonify({"error": "File size exceeds the maximum limit"}), 400

        video_duration = get_video_duration(video_path)
        if not (Config.MIN_VIDEO_DURATION_SECS <= video_duration <= Config.MAX_VIDEO_DURATION_SECS):
            return jsonify({"error": "Video duration out of range"}), 400

        new_video = Video(filename=filename, file_size=file_size, duration=video_duration)
        db.session.add(new_video)
        db.session.commit()

        return jsonify({"message": "Video uploaded successfully", "id": new_video.id}), 201
    else:
        return jsonify({"error": "Invalid file type"}), 400

@video_bp.route('/trim/<int:video_id>', methods=['POST'])
def trim_video(video_id):
    token = request.headers.get('Authorization')
    if token != "Bearer " + Config.API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    
    video = Video.query.get_or_404(video_id)
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')

    if not start_time or not end_time:
        return jsonify({"error": "Start and end times must be provided"}), 400

    trimmed_video_path = trim_video_file(video.filename, start_time, end_time)

    return jsonify({"message": "Video trimmed", "path": trimmed_video_path}), 200
