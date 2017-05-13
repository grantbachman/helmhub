from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Profile, Chart, ChartVersion
import tempfile
import io


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

    """
    TODO: Make this an API Integration test so I can actually
    override the default MEDIA ROOT

    def test_create(self):
        v = '0.1.0'
        tmpdir = tempfile.TemporaryDirectory()
        with self.settings(MEDIA_ROOT=tmpdir.name):
            f = SimpleUploadedFile(f'test-{v}.tgz', b'Line 1\nLine 2')
            version = ChartVersion(version=v, tgz=f, chart=self.chart)
            version.save()
        assert ChartVersion.objects.first() == version
        import pdb; pdb.set_trace()
        assert version.tgz is None
    """


class TestChartAPI(TestCase):

    fixtures = ['tests/fixtures/testuser']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        profile = Profile.objects.first()
        chart = Chart(name='Test Chart', profile=profile)
        self.chart = chart.save()

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
