# tests/test_auth.py

import unittest
from app import create_app

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_token(self):
        response = self.client.post('/upload', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

    def test_valid_token(self):
        # POST request to the /upload endpoint with a valid token and file
        response = self.client.post(
            '/upload',
            data={'video': (open('test_videos/test_video_dummy.mp4', 'rb'), 'test_video_dummy.mp4')},
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
