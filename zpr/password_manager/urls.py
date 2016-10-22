from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^add-password/$', views.do_login, name='add-password'),
    url(r'^edit-password/(?P<id>[0-9]*)/$', views.do_login, name='edit-password'),
    url(r'^delete-password/(?P<id>[0-9]*)$', views.do_login, name='delete-password')
]
