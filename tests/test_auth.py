# Tests for authentication
import unittest
from app import create_app

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_token(self):
        response = self.client.get('/upload', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

    def test_valid_token(self):
        response = self.client.get('/upload', headers={'Authorization': 'Bearer <TOKEN>'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
