# tests/test_auth.py

import unittest
import os
from app import create_app

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.api_token = os.getenv('API_TOKEN', 'hardcoded_token_12345')

    def test_invalid_token(self):
        response = self.client.post('/upload', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

    def test_valid_token(self):
        # POST request to the /upload endpoint with a valid token and file
        response = self.client.post(
            '/upload',
            data={'video': (open('test_videos/test_video_dummy.mp4', 'rb'), 'test_video_dummy.mp4')},
            headers={'Authorization': f'Bearer {self.api_token}'},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
