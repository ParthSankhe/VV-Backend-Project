# # Utility functions like video trimming, merging, and generating shareable links
# import os
# from moviepy.video.io.VideoFileClip import VideoFileClip

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}

# def save_video_file(video, filename):
#     # defining the directory where you want to save the video
#     upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    
#     # creating the directory if it doesn't exist
#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)
    
#     video_path = os.path.join(upload_folder, filename)
#     video.save(video_path)
#     return video_path

# def get_video_duration(video_path):
#     clip = VideoFileClip(video_path)
#     return clip.duration

# def trim_video_file(filename, start_time, end_time):
#     # Define the path where uploaded videos are saved
#     upload_folder = os.path.join(os.getcwd(), 'app', 'uploaded_files')
    
#     # Construct the full path for the video file
#     video_path = os.path.join(upload_folder, filename)
    
#     # Verify that the video file exists
#     if not os.path.exists(video_path):
#         raise FileNotFoundError(f"Video file not found: {video_path}")
    
#     # Process the video
#     with VideoFileClip(video_path) as clip:
#         # Define output path for trimmed video
#         trimmed_video_path = os.path.join(upload_folder, f"trimmed_{filename}")
        
#         # Trim the video
#         trimmed_clip = clip.subclip(start_time, end_time)
#         trimmed_clip.write_videofile(trimmed_video_path, codec='libx264')
        
#     return trimmed_video_path

# Utility functions like video trimming, merging, and generating shareable links
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}

def save_video_file(video, filename):
    # Define the directory where you want to save the video
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploaded_files')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    video_path = os.path.join(upload_folder, filename)
    video.save(video_path)
    return video_path

def get_video_duration(video_path):
    clip = VideoFileClip(video_path)
    return clip.duration

def trim_video_file(filename, start_time, end_time):
    # Define the path where uploaded videos are saved
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploaded_files')
    
    # Construct the full path for the video file
    video_path = os.path.join(upload_folder, filename)
    
    # Verify that the video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Process the video
    with VideoFileClip(video_path) as clip:
        # Define output path for trimmed video
        trimmed_video_path = os.path.join(upload_folder, f"trimmed_{filename}")
        
        # Trim the video
        trimmed_clip = clip.subclip(start_time, end_time)
        trimmed_clip.write_videofile(trimmed_video_path, codec='libx264')
        
    return trimmed_video_path

