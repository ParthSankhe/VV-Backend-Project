# Video Processing API

This project is a Flask-based API for uploading, trimming, merging, and sharing video files. It is built with REST principles, using SQLite as a database, and MoviePy for video processing. 

## Features
1. **Video Upload:**
   - Upload video files with configurable size and duration limits.
   - Stores metadata such as video file size and duration in the database.

2. **Video Trimming:**
   - Allows trimming of uploaded videos by specifying start and end times.

3. **Video Merging:**
   - Merges multiple uploaded videos into one file.

4. **Link Sharing:**
   - Generates time-based shareable links for uploaded videos.

5. **Validation:**
   - Verifies if a shareable link is valid and hasn't expired.

## Assumptions and Choices

1. **Video Size and Duration Limits:**
   - The maximum video size allowed is **50 MB**, and video durations must be between **3** and **30 seconds**.
   - These limits were chosen to prevent excessively large uploads on a demo application. They can be modified in the `Config` class (`config.py`).

2. **SQLite Database:**
   - SQLite was chosen as the database for simplicity and ease of use in a local development environment. It supports all required functionality for this API without the need for complex database setups.

3. **Hardcoded API Token:**
   - The API token is hardcoded for simplicity in the `config.py` file, but in a production environment, it should be dynamically set through environment variables for security purposes.

4. **Video Storage Location:**
   - Videos are stored in the `uploaded_files` folder, and this folder is excluded from version control via the `.gitignore` file to prevent accidental commits of actual video data.

5. **Exception Handling:**
   - Appropriate exception handling is implemented for scenarios like missing files, invalid input parameters, and unauthorized requests.


## Setup Instructions

### Prerequisites

- **Python Version**: Python 3.8 or higher is required.
- **Virtual Environment**: Using a virtual environment is recommended but optional.

### Installation

1. **Clone the Repository**

   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Set Up Virtual Environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   The database is automatically configured to use SQLite. No additional setup is required unless you want to switch to another database.

5. **Environment Variables:**
   The API token can be set dynamically:
   ```bash
   export API_TOKEN='your_token_here'
   ```

6. **Run the application:**
   ```bash
   flask run
   ```

7. **Run tests:**
   ```bash
   pytest
   ```


## API Endpoints

### 1. **Upload Video**
- **URL**: `/upload`
- **Method**: `POST`
- **Authorization**: API Token (`Bearer token`)
- **Request Body**: Form Data (with video file)
  - `video`: Video file to upload.
- **Response**:
  - `201 Created`:
    ```json
    {
      "message": "Video uploaded successfully",
      "id": 1
    }
    ```
  - `400 Bad Request` for:
    - No video file.
    - Invalid file type.
    - Video file size exceeds the limit.
    - Video duration out of range.
  - `401 Unauthorized` for invalid token.

### 2. **Trim Video**
- **URL**: `/trim/<int:video_id>`
- **Method**: `POST`
- **Authorization**: API Token (`Bearer token`)
- **Request Body (JSON)**:
  ```json
  {
    "start_time": 3.5,
    "end_time": 10
  }
  ```
- **Response**:
  - `200 OK`:
    ```json
    {
      "message": "Video trimmed",
      "path": "/path/to/trimmed_video.mp4"
    }
    ```
  - `400 Bad Request` for:
    - Missing start or end times.
    - Invalid time range.
  - `404 Not Found` if the video does not exist.
  - `401 Unauthorized` for invalid token.

### 3. **Merge Videos**
- **URL**: `/merge`
- **Method**: `POST`
- **Authorization**: API Token (`Bearer token`)
- **Request Body (JSON)**:
  ```json
  {
    "video_ids": [1, 2]
  }
  ```
- **Response**:
  - `200 OK`:
    ```json
    {
      "message": "Videos merged successfully",
      "path": "/path/to/merged_video.mp4"
    }
    ```
  - `400 Bad Request` for:
    - Missing `video_ids`.
    - No videos found to merge.
  - `401 Unauthorized` for invalid token.

### 4. **Share Link**
- **URL**: `/share`
- **Method**: `POST`
- **Authorization**: API Token (`Bearer token`)
- **Request Body (JSON)**:
  ```json
  {
    "video_id": 2,
    "expiry_time": 145
  }
  ```
- **Response**:
  - `200 OK`:
    ```json
    {
      "message": "Shareable link generated",
      "link": "http://localhost:5000/validate_link?link=some_unique_id"
    }
    ```
  - `400 Bad Request` for missing `video_id` or `expiry_time`.
  - `401 Unauthorized` for invalid token.

### 5. **Validate Link**
- **URL**: `/validate_link`
- **Method**: `POST`
- **Request Body (JSON)**:
  ```json
  {
    "link": "http://localhost:5000/validate_link?link=some_unique_id"
  }
  ```
- **Response**:
  - `200 OK` if the link is valid:
    ```json
    {
      "message": "Link is valid"
    }
    ```
  - `400 Bad Request` for:
    - Missing link.
    - Expired or invalid link.

## API Documentation

### Postman Collection

A Postman collection of the API endpoints is available [here](docs/Video API Project.postman_collection.json). You can import this file into Postman to interact with the API and view the documentation directly within Postman.

## Citations

During the development of this project, the following resources were referred to:

1. **Flask Documentation**  
   Official Flask documentation was used for setting up the Flask app, routing, and managing requests.  
   [Flask Documentation](https://flask.palletsprojects.com/en/latest/)

2. **MoviePy Documentation**  
   Used for handling video file manipulations like trimming and merging.  
   [MoviePy Documentation](https://zulko.github.io/moviepy/)

3. **SQLite Documentation**  
   Referred to for integrating SQLite as the database.  
   [SQLite Documentation](https://sqlite.org/docs.html)

4. **Werkzeug Documentation**  
   Utilized for utilities like `secure_filename` to handle file uploads securely.  
   [Werkzeug Documentation](https://werkzeug.palletsprojects.com/en/latest/)

5. **SQLAlchemy Documentation**  
   Used for database integration and ORM functionality.  
   [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/)

6. **WTForms Documentation**  
   Referred to when handling forms in the application.  
   [WTForms Documentation](https://wtforms.readthedocs.io/en/latest/)

7. **ChatGPT (OpenAI)**  
   Used for syntax correction, generating boilerplate code and debugging assistance throughout the development process.


## Exception Handling
- Each endpoint has appropriate error handling, including cases for invalid input, unauthorized access, missing files, and file size limits.

- **Examples:**
  - 400 error for invalid video file type or exceeding size/duration limits.
  - 401 error for missing or invalid API tokens.
  - 404 error when a video ID is not found in the database.

## Future Improvements
- Switch to a more secure and dynamic authentication method (e.g., OAuth).
- Use a cloud-based storage system to handle larger video file sizes.
