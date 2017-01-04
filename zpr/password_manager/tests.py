from django.test import TestCase, Client
from django.contrib.auth.models import User
import pytest

# Create your tests here.
from password_manager.models import PasswordEntry


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_not_logged_in_user_cant_open_restricted_access_pages(self):
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

    def test_user_can_add_password(self):
        User.objects.create_user(username='test', password='test')
        assert self.client.login(username='test', password='test') == True
        p = PasswordEntry(name="bob", password="bob1", username="kowalsky")
        p.save()
        data = {"name": "asd", "username": "asd1", "password": "asdPass"}
        c = Client()
        response = c.post('/add-password/', data)
        passwords = PasswordEntry.objects.all()
        self.assertEqual(len(passwords), 1)
        assert response.status_code == 302

    # def test_user_can_delete_password(self):
    #     User.objects.create_user(username='test', password='test')
    #     assert self.client.login(username='test', password='test') == True
    #     data = {"name": "asd", "username": "asd1", "password": "asdPass"}
    #     c = Client()
    #     response = c.post('/add-password/', data)
    #     assert response.status_code == 302
    #     response = c.post('/delete-password/1/')
    #     assert response.status_code == 302

    def test_user_can_logout(self):
        User.objects.create_user(username='test', password='test')
        assert self.client.login(username='test', password='test') == True
        c = Client()
        response = c.post('/logout/')
        assert response.status_code == 200

    def test_user_can_open_registartion_page(self):
        c = Client()
        response = c.get('/register/')
        assert response.status_code != 404
        assert response.status_code != 403
        assert response.content != ""

    @pytest.mark.django_db
    def test_user_can_register(self):
        c = Client()
        data = {'username': 'bob',
                'password1': 'asd123zxc456',
                'password2': 'asd123zxc456'
                }
        response = c.post('/register/', data)
        assert response.status_code == 302
        user = User.objects.get(id=1)
        assert user.username == 'bob'

    @pytest.mark.django_db
    def test_user_can_login(self):
        User.objects.create_user(username='test', password='test')
        c = Client()
        assert c.login(username = 'test', password = 'test') == True
        response = c.get("/")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_cant_login_if_not_have_account(self):
        c = Client()
        assert c.login(username = 'test', password = 'test') == False

