from django.contrib.auth.models import User
from django.test import Client, TestCase

from projects.models import Project


class DashboardTestCase(TestCase):

    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        username, password = 'Expert', 'expert123A'
        User.objects.create_user(username=username, email='info@nashlombard.ru', password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_dashboard_requires_authentication(self):

        # Anonymous users can't see the dashboard

        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')

        # Authenticated users can see the dashboard

        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_projects_on_dashboard(self):

        # There are 3 projects on the dashboard (loaded from the fixtures)

        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(len(projects), 3)


class ProjectsTestCase(TestCase):
    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        self.projects = Project.objects.order_by('id')

    def test_project_has_ended(self):

        # 2 of the projects have ended
        self.assertListEqual([p.has_ended for p in self.projects], [True, True, False])

    def test_project_is_over_budget(self):

        # 1 of the projects is over budget
        self.assertListEqual([p.is_over_budget for p in self.projects], [True, False, False])

    def test_total_estimated_hours(self):

        self.assertListEqual([p.total_estimated_hours for p in self.projects], [690, 170, 40])

    def test_total_actual_hours(self):

        self.assertListEqual([p.total_actual_hours for p in self.projects], [739, 60, 5])
