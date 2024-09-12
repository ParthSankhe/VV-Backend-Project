# tests/test_videos.py

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
        video_path = os.path.join('test_videos', 'test_video_dummy.mp4')
        response = self.client.post(
            '/upload',
            data={'video': (open(video_path, 'rb'), 'test_video_dummy.mp4')},
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 201)
        self.video_id = response.json['id']

    def test_trim_video(self):
        # Upload a video first
        self.test_upload_video()

        # Trim the video
        response = self.client.post(
            f'/trim/{self.video_id}',
            json={'start_time': 3, 'end_time': 10},
            headers={'Authorization': 'Bearer hardcoded_token_12345'}
        )
        
        # Print the response data for debugging
        print("Trim Video Response Status Code:", response.status_code)
        print("Trim Video Response Data:", response.data)
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_merge_videos(self):
        # Upload two videos first
        video_path1 = os.path.join('test_videos', 'test_video_dummy.mp4')
        response1 = self.client.post(
            '/upload',
            data={'video': (open(video_path1, 'rb'), 'test_video_1.mp4')},
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            content_type='multipart/form-data'
        )
        video_id1 = response1.json['id']

        video_path2 = os.path.join('test_videos', 'test_video_dummy.mp4')
        response2 = self.client.post(
            '/upload',
            data={'video': (open(video_path2, 'rb'), 'test_video_2.mp4')},
            headers={'Authorization': 'Bearer hardcoded_token_12345'},
            content_type='multipart/form-data'
        )
        video_id2 = response2.json['id']

        # Merge the videos
        response = self.client.post(
            '/merge',
            json={'video_ids': [video_id1, video_id2]},
            headers={'Authorization': 'Bearer hardcoded_token_12345'}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
