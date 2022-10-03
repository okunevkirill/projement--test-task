from django.conf.urls import url

from projects.views import (
    AssignmentView, DashboardView, ProjectUpdateView,
    export_dashboard_file_view, download_file_view,
)

urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^export-dashboard-file/', export_dashboard_file_view, name='export-dashboard-file'),
    url(r'^download-dashboard-file/', download_file_view, name='download-dashboard-file'),
]
