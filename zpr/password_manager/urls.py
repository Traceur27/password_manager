from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^me/$', views.profile, name='profile'),
    url(r'^me/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^me/change-password/$', views.password_change,
        name='change-password'),
    url(r'^me/change-password-done/$',
        auth_views.password_change_done, name='password_change_done'),
    url(r'^me/remove/$', views.remove_account, name='remove_account'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^add-password/$', views.add_password_entry, name='add-password'),
    url(r'^edit-password/(?P<id>[0-9]*)/$',
        views.edit_password, name='edit-password'),
    url(r'^delete-password/(?P<id>[0-9]*)/$',
        views.delete_password, name='delete-password')
]
