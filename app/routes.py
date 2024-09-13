from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.models import db, Video
from app.config import Config
from app.utils import allowed_file, save_video_file, get_video_duration, trim_video_file, merge_videos, generate_shareable_link, validate_shareable_link

video_bp = Blueprint('video_bp', __name__)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    try:
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
    except Exception as e:
        return jsonify({"error": f"An error occurred during upload: {str(e)}"}), 500

@video_bp.route('/trim/<int:video_id>', methods=['POST'])
def trim_video(video_id):
    try:
        token = request.headers.get('Authorization')
        if token != "Bearer " + Config.API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        
        video = Video.query.get_or_404(video_id)
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')

        if not start_time or not end_time:
            return jsonify({"error": "Start and end times must be provided"}), 400

        if start_time < 0 or end_time <= start_time:
            return jsonify({'error': 'Invalid time range'}), 400

        trimmed_video_path = trim_video_file(video.filename, start_time, end_time)

        return jsonify({"message": "Video trimmed", "path": trimmed_video_path}), 200
    except FileNotFoundError as fnf_error:
        return jsonify({"error": str(fnf_error)}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred during trimming: {str(e)}"}), 500

@video_bp.route('/merge', methods=['POST'])
def merge_videos_route():
    try:
        token = request.headers.get('Authorization')
        if token != "Bearer " + Config.API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        
        video_ids = request.json.get('video_ids')
        if not video_ids:
            return jsonify({"error": "Video IDs must be provided"}), 400

        video_files = [Video.query.get_or_404(video_id).filename for video_id in video_ids]

        if not video_files:
            return jsonify({"error": "No videos found to merge"}), 400

        merged_video_path = merge_videos(video_files)

        return jsonify({"message": "Videos merged successfully", "path": merged_video_path}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred during merge: {str(e)}"}), 500

@video_bp.route('/share', methods=['POST'])
def share_link_route():
    try:
        token = request.headers.get('Authorization')
        if token != "Bearer " + Config.API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        
        video_id = request.json.get('video_id')
        expiry_time = request.json.get('expiry_time')

        if not video_id or not expiry_time:
            return jsonify({"error": "Video ID and expiry time must be provided"}), 400

        link = generate_shareable_link(video_id, expiry_time)

        return jsonify({"message": "Shareable link generated", "link": link}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while generating the link: {str(e)}"}), 500

@video_bp.route('/validate_link', methods=['POST'])
def validate_link_route():
    try:
        link = request.json.get('link')
        
        if not link:
            return jsonify({"error": "Link must be provided"}), 400

        is_valid = validate_shareable_link(link)

        if is_valid:
            return jsonify({"message": "Link is valid"}), 200
        else:
            return jsonify({"error": "Link is expired or invalid"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred during link validation: {str(e)}"}), 500

