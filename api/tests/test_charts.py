from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Profile, Chart, ChartVersion
from django.conf import settings
import tempfile
import os


class TestChart(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        self.user_profile = Profile.objects.first()

    def test_create(self):
        chart = Chart(profile=self.user_profile)
        chart.save()
        charts = self.user_profile.chart_set.all()
        assert len(charts) == 1
        assert charts[0] == chart


class TestVersion(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        user_profile = Profile.objects.first()
        self.chart = Chart(profile=user_profile)
        self.chart.save()


class TestChartAPI(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

        profile = Profile.objects.first()
        self.chart = Chart(name='Test Chart', profile=profile)
        self.chart.save()

    def test_charts(self):
        assert Chart.objects.count() == 1

        # Test index
        resp = self.client.get('/charts')
        assert resp.status_code == 200
        assert resp.data['results'][0]['name'] == 'Test Chart'

        # Test single
        id_ = resp.data['results'][0]['id']
        resp = self.client.get(f'/charts/{id_}')
        assert resp.status_code == 200
        assert resp.data.get('name') == 'Test Chart'

    def test_upload_invalid_chart_id(self):
        resp = self.client.post('/charts/999/upload', data={})
        assert resp.status_code == 404

    def test_upload_valid_chart(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.settings(MEDIA_ROOT=tmpdir):
                with open('tests/fixtures/testchart-0.1.0.tgz', 'rb') as f:
                    chart_id = self.chart.id
                    resp = self.client.post(f'/charts/{chart_id}/upload', {'file': f}, format='multipart')
            # File should be uploaded into charts subdir
            assert os.path.isfile(os.path.join(tmpdir, 'charts/testchart-0.1.0.tgz'))
        assert resp.status_code == 201
        version = self.chart.versions.first()
        # version should be parsed correctly
        assert version.version == '0.1.0'


class TestVersionAPI(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        profile = Profile.objects.first()
        self.chart = Chart(name='Test Chart', profile=profile)
        self.chart.save()
        version = ChartVersion(version='0.1.0', chart=self.chart)
        version.save()

    def test_version(self):
        assert ChartVersion.objects.count() == 1
        chart_id = self.chart.id
        resp = self.client.get(f'/charts/{chart_id}/versions')
        assert resp.status_code == 200
        version_id = resp.data['results'][0]['id']
        resp = self.client.get(f'/charts/{chart_id}/versions/{version_id}')
        assert resp.status_code == 200
        assert resp.data['version'] == '0.1.0'
