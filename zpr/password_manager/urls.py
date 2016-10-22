from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.login, name='logout'),
    url(r'^add-password/$', views.login, name='add-password'),
    url(r'^edit-password/(?P<id>[0-9]*)/$', views.login, name='edit-password'),
    url(r'^delete-password/(?P<id>[0-9]*)$', views.login, name='delete-password')
]
