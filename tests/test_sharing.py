# Unit and end-to-end tests for link sharing

import unittest
from app import create_app, db
from io import BytesIO
import os
import time

class LinkSharingTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_generate_shareable_link(self):
        # Assuming a video with ID 1 exists
        video_id = 1
        expiry_time = 60  # Link expires in 60 seconds
        
        response = self.client.post(
            '/share',
            json={'video_id': video_id, 'expiry_time': expiry_time},
            headers={'Authorization': 'Bearer hardcoded_token_12345'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('link', response.json)

        link = response.json['link']
        time.sleep(1)  # Wait a bit before validation

        validate_response = self.client.post(
            '/validate_link',
            json={'link': link}
        )

        self.assertEqual(validate_response.status_code, 200)

    def test_invalid_shareable_link(self):
        invalid_link = 'http://example.com/validate_link?link=invalid_link_id'
        response = self.client.post(
            '/validate_link',
            json={'link': invalid_link}
        )

        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
