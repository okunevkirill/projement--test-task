from django.forms.models import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from projects.models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['actual_design', 'actual_development', 'actual_testing']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))
