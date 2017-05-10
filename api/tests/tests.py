from django.test import TestCase
from rest_framework.test import RequestsClient, APIClient
from django.contrib.auth.models import User
from io import BytesIO
import gzip


client = APIClient()


class TestAPI(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def test_unauthorized(self):
        resp = APIClient().get('/')  # Create not-logged-in client
        assert resp.status_code == 401

    def test_authorized(self):
        resp = self.client.get('/')
        assert resp.status_code == 200

    def test_upload_file(self):
        s = BytesIO()
        with gzip.GzipFile(fileobj=s, mode='xb') as g:
            g.write(b'Line 1.\nLine 2.')
        data = s.getvalue()
        resp = self.client.put('/upload/file_to_upload.txt.gz', format='multipart', data=data)
        assert resp.status_code == 204
