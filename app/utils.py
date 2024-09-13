# Utility functions like video trimming, merging, and generating shareable links
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import uuid
import time
from flask import current_app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}

def save_video_file(video, filename):
    try:
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploaded_files')
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        video_path = os.path.join(upload_folder, filename)
        video.save(video_path)
        return video_path
    except Exception as e:
        raise IOError(f"Error saving video file: {str(e)}")

def get_video_duration(video_path):
    try:
        clip = VideoFileClip(video_path)
        return clip.duration
    except Exception as e:
        raise IOError(f"Error retrieving video duration: {str(e)}")

def trim_video_file(filename, start_time, end_time):
    try:
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploaded_files')
        video_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        with VideoFileClip(video_path) as clip:
            trimmed_video_path = os.path.join(upload_folder, f"trimmed_{filename}")
            trimmed_clip = clip.subclip(start_time, end_time)
            trimmed_clip.write_videofile(trimmed_video_path, codec='libx264')
        
        return trimmed_video_path
    except FileNotFoundError as fnf_error:
        raise fnf_error
    except Exception as e:
        raise RuntimeError(f"Error trimming video: {str(e)}")

def merge_videos(filenames):
    try:
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploaded_files')
        video_clips = [VideoFileClip(os.path.join(upload_folder, filename)) for filename in filenames]

        if not video_clips:
            raise ValueError("No videos to merge.")

        merged_video_path = os.path.join(upload_folder, "merged_video.mp4")
        final_clip = concatenate_videoclips(video_clips)
        final_clip.write_videofile(merged_video_path, codec='libx264')

        return merged_video_path
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Error merging videos: {str(e)}")

def generate_shareable_link(video_id, expiry_time):
    try:
        link_id = uuid.uuid4().hex
        expiry_timestamp = time.time() + expiry_time
        shareable_link = f"{current_app.config['BASE_URL']}/validate_link?link={link_id}"
        
        # Save the link and expiry time in a datastore (e.g., database or in-memory cache)
        # For simplicity, let's use a file-based approach here
        with open("shareable_links.txt", "a") as f:
            f.write(f"{link_id},{video_id},{expiry_timestamp}\n")
        
        return shareable_link
    except Exception as e:
        raise IOError(f"Error generating shareable link: {str(e)}")

def validate_shareable_link(link):
    try:
        link_id = link.split("link=")[-1]
        
        with open("shareable_links.txt", "r") as f:
            lines = f.readlines()
        
        for line in lines:
            link_info = line.strip().split(",")
            if link_info[0] == link_id:
                video_id = link_info[1]
                expiry_timestamp = float(link_info[2])
                if time.time() < expiry_timestamp:
                    return True
        
        return False
    except Exception as e:
        raise IOError(f"Error validating link: {str(e)}")



