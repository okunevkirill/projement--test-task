from decimal import Decimal

from django.test import TestCase

from projects.models import Company, Project, ProjectTag


class TestCompanyModel(TestCase):
    def test_model_str(self):
        name = 'Horns and hooves'
        company = Company.objects.create(name=name)
        self.assertEqual(str(company), name)


class TestProjectModel(TestCase):
    fixtures = ['projects/fixtures/test_db.json']

    def setUp(self):
        self.projects = Project.objects.order_by('id')
        self.project = self.projects[0]

    def test_model_str(self):
        self.assertEqual(str(self.project), '{}'.format(self.project.title))

    def test_project_has_ended(self):
        # 3 of the projects have ended
        self.assertListEqual(
            [p.has_ended for p in self.projects], [True, True, False, True])

    def test_project_is_over_budget(self):
        # 1 of the projects is over budget
        self.assertListEqual(
            [p.is_over_budget for p in self.projects], [True, False, False, False])

    def test_total_estimated_hours(self):
        self.assertListEqual(
            [p.total_estimated_hours for p in self.projects],
            [690, 170, 40.00, 30.00])

    def test_total_actual_hours(self):
        self.assertListEqual(
            [p.total_actual_hours for p in self.projects],
            [Decimal('739.00'), Decimal('60.00'), Decimal('5.00'), Decimal('3.00')])


class TestProjectTagModel(TestCase):
    def test_model_str(self):
        title = '@work_hard'
        tag = ProjectTag.objects.create(title=title)
        self.assertEqual(str(tag), title)
