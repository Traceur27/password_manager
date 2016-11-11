from django.test import TestCase, Client
from django.contrib.auth.models import User
import pytest

# Create your tests here.


def test_not_logged_in_user_cant_open_restricted_access_pages():
    c = Client()
    response = c.get('/')
    assert response.status_code == 302
    response = c.get('/me/')
    assert response.status_code == 302
    response = c.get('/me/edit/')
    assert response.status_code == 302
    response = c.get('/me/change-password/')
    assert response.status_code == 302
    response = c.get('/me/change-password-done/')
    assert response.status_code == 302
    response = c.get('/add-password/')
    assert response.status_code == 302
    response = c.get('/edit-password/1')
    assert response.status_code == 301
    response = c.get('/delete-password/1')
    assert response.status_code == 302


def test_user_can_open_registartion_page():
    c = Client()
    response = c.get('/register/')
    assert response.status_code != 404
    assert response.status_code != 403
    assert response.content  != ""


@pytest.mark.django_db
def test_user_can_register():
    c = Client()
    data = {'username': 'bob',
            'password1': 'asd123zxc456',
            'password2': 'asd123zxc456'
            }
    response = c.post('/register/', data)
    assert response.status_code == 302
    user = User.objects.get(id=1)
    assert user.username == 'bob'
