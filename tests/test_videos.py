# Unit and end-to-end tests for video-related APIs

import unittest
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
        # Path to the test video
        test_video_path = os.path.join(os.path.dirname(__file__), '../test_videos/test_video.mp4')
        
        # Open the video file for testing upload
        with open(test_video_path, 'rb') as video:
            response = self.client.post('/upload', 
                data={'video': video}, 
                headers={'Authorization': 'Bearer <TOKEN>'}
            )
            self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()

