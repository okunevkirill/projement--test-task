import shutil
import tempfile

from pathlib import Path
from django.conf import settings
from django.utils import timezone
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from projects.models import Project
from projement import celery_app


class BaseTask(celery_app.Task):
    ignore_result = False

    def __call__(self, *args, **kwargs):
        print('Starting {}'.format(self.name))
        return self.run(*args, **kwargs)

    def after_return(self, *args, **kwargs):
        # exit point of the task whatever is the state
        print('End of {}'.format(self.name))

    def run(self, *args, **kwargs):
        raise NotImplementedError(
            "Define 'run' in class {}".format(self.__class__.__name__))


class ExportDashboardIntoExcelTask(BaseTask):
    @staticmethod
    def create_row(instance: Project):
        return (
            instance.title,
            instance.all_tags,
            instance.company.name,
            instance.total_estimated_hours,
            instance.total_actual_hours,
        )

    def create_workbook(self, workbook: Workbook):
        queryset = Project.objects.all()
        sheet = workbook.active
        for index, instance in enumerate(queryset):
            sheet.append(self.create_row(instance))
        return workbook

    @staticmethod
    def copy_and_get_copied_path():
        template_path = Path(settings.BASE_DIR, 'static', 'docs', 'dashboard_template.xlsx')
        destination_path = '%s/%s_exported_dashboard.xlsx' % (tempfile.gettempdir(), int(timezone.now().timestamp()))
        shutil.copy(template_path, destination_path)
        return destination_path

    def run(self, *args, **kwargs):
        destination_path = self.copy_and_get_copied_path()
        workbook = load_workbook(destination_path)
        workbook = self.create_workbook(workbook)
        workbook.save(filename=destination_path)
        return {
            'detail': 'Successfully export dashboard',
            'data': {
                'outfile': destination_path
            }
        }


export_dashboard_task = celery_app.register_task(ExportDashboardIntoExcelTask())
