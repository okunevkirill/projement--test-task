from django.conf.urls import url
from django.contrib.auth import views as django_auth_views

from auth.views import login


urlpatterns = [
    url(r'login/$', login, name='login'),
    url(r'logout/$', django_auth_views.logout_then_login, name='logout'),
]
