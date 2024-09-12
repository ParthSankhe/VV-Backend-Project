# Tests for authentication
import unittest
from io import BytesIO
from app import create_app

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_token(self):
        # POST request to the /upload endpoint with an invalid token
        response = self.client.post('/upload', headers={'Authorization': 'Bearer invalid_token'})
        # Expecting a 401 Unauthorized response for invalid tokens
        self.assertEqual(response.status_code, 401)

    def test_valid_token(self):
        # POST request to the /upload endpoint with a valid token but missing file
        data = {
            'video': (BytesIO(b"fake_video_content"), 'test_video.mp4')
        }
        response = self.client.post(
            '/upload',
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            data=data,
            content_type='multipart/form-data'
        )
        # Expecting a 200 OK response for valid tokens
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()


