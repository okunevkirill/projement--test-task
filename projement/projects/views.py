import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models.functions import Lower
from django.http import Http404
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from markdown import markdown

from projects.forms import ProjectForm
from projects.models import Project, IsNotNull, ProjectHistory


class AssignmentView(TemplateView):
    template_name = 'projects/assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'README.md'), encoding='utf-8') as f:
            assignment_content = f.read()

        context.update({
            'assignment_content': mark_safe(markdown(assignment_content))
        })

        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    ordering = (IsNotNull('end_date'), '-end_date', Lower('title'))
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        projects = super().get_queryset()
        projects = projects.select_related('company')

        return projects


class ProjectUpdateView(LoginRequiredMixin, FormView):
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        if 'all_tags' not in kwargs:
            kwargs['all_tags'] = self.object.all_tags
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.object = Project.objects.filter(pk=pk).first()
        if not self.object or self.object.get_absolute_url() != request.path:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not any(form.cleaned_data.values()):
            # There were no changes
            return super(ProjectUpdateView, self).form_valid(form)

        # There were changes at least 1 value
        history_data = {'project': self.object, 'user': self.request.user}
        initial_values, delta_values, resulting_value = {}, {}, {}
        for key, value in form.cleaned_data.items():
            initial_values[key] = getattr(self.object, key)
            delta_values[key] = value
            resulting_value[key] = initial_values[key] + delta_values[key]
            setattr(self.object, key, F(key) + value)
        self.object.save()
        history_data['info'] = 'initial={}\ndelta={}\nresulting={}'.format(
            initial_values, delta_values, resulting_value)
        ProjectHistory.objects.create(**history_data)
        return super(ProjectUpdateView, self).form_valid(form)
