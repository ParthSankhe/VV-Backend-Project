# Unit and end-to-end tests for video-related APIs

import unittest
from io import BytesIO
from app import create_app, db
import os

class VideoUploadTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_upload_video(self):
        # Create a fake video file in memory
        video_data = BytesIO(b"fake_video_content")
        
        # Perform a POST request to upload the video with valid token
        response = self.client.post(
            '/upload',
            data={'video': (video_data, 'test_video.mp4')},
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            content_type='multipart/form-data'  # Important for file uploads
        )

        # Expecting 201 Created response for successful upload
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()


