from pathlib import Path
from unittest.mock import patch, MagicMock

from celery.result import AsyncResult
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from projects.models import Project
from projects.tasks import export_dashboard_task


class TestProjectsViews(TestCase):
    fixtures = ['projects/fixtures/test_db.json']

    def setUp(self):
        super().setUp()

        username, password = 'Expert', 'expert123A'
        get_user_model().objects.create_user(
            username=username, email='info@nashlombard.ru', password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)
        self.project = Project.objects.order_by('id').first()

    def test_dashboard_requires_authentication(self):
        # Anonymous users can't see the dashboard
        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')

        # Authenticated users can see the dashboard
        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_projects_on_dashboard(self):
        # There are 4 projects on the dashboard (loaded from the fixtures)
        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(len(projects), 4)

    def test_project_update_requires_authentication(self):
        # Anonymous users cannot update the project
        client = Client()
        url = self.project.get_absolute_url()
        response = client.get(url)
        self.assertRedirects(response, '/login/?next=/projects/1-gateme/')

        # Authenticated users can update the project
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_update_incorrect_id(self):
        url = '/projects/42-gateme/'
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_project_update_post_request(self):
        url = self.project.get_absolute_url()

        # Sending null data
        response = self.authenticated_client.post(url, data={
            'actual_design': 0, 'actual_development': 0, 'actual_testing': 0})
        self.assertRedirects(response, '/dashboard/')

        # Sending correct data
        response = self.authenticated_client.post(url, data={
            'actual_design': 1, 'actual_development': 1, 'actual_testing': 1})
        self.assertRedirects(response, '/dashboard/')

    @patch.object(export_dashboard_task, 'delay')
    def test_export_dashboard_file_view(self, mock_celery_delay):
        task = MagicMock()
        task.id = 42
        mock_celery_delay.return_value = task

        url = '/export-dashboard-file/'
        client = Client()
        response = client.get(url)
        self.assertRedirects(response, '/login/?next={}'.format(url))

        # Requests not available via get method
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.authenticated_client.post(url)
        self.assertEqual(response.status_code, 202)

    @patch.object(AsyncResult, 'get')
    def test_download_file_view(self, mock_celery_async_get):
        file_name = 'file_for_del.tmp'
        self.assertFalse(Path(file_name).exists())

        mock_celery_async_get.return_value = {'data': {'outfile': file_name}}

        url = '/download-dashboard-file/'
        client = Client()
        response = client.get(url)
        self.assertRedirects(response, '/login/?next={}'.format(url))

        response = self.authenticated_client.get(url, data={'task_id': 42})
        self.assertEqual(response.status_code, 404)
