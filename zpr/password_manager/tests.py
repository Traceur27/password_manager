from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
from password_manager.models import PasswordEntry


class PasswordManagerTests(TestCase):

    # utwórz i zaloguj uzytkownika
    def get_logged_in_client(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        data = {"username": "test", "password": "test"}
        c.post('/login/', data)
        return c

    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_not_logged_in_user_cant_open_restricted_access_pages(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/me/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/me/edit/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/me/change-password/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/me/change-password-done/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/add-password/')
        self.assertEquals(response.status_code, 302)
        response = c.get('/edit-password/1')
        self.assertEquals(response.status_code, 301)
        response = c.get('/delete-password/1')
        self.assertEquals(response.status_code, 302)

    def test_user_can_add_password(self):
        c = self.get_logged_in_client()
        # utwórz obiekt w bazie danych
        data = {"name": "asd", "username": "asd1", "password": "asdPass"}
        response = c.post('/add-password/', data)
        passwords = PasswordEntry.objects.all()
        self.assertEqual(len(passwords), 1)
        self.assertEquals(response.status_code, 302)

    def test_user_can_delete_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        data = {"answer":"yes"}
        response = c.post('/delete-password/' + psw.id.__str__(), data)
        self.assertEquals(response.status_code, 302)
        response = c.get('/delete-password/' + psw.id.__str__())
        self.assertEquals(response.status_code, 404)

    def test_user_can_logout(self):
        User.objects.create_user(username='test', password='test')
        self.assertEquals(self.client.login(username='test', password='test'), True)
        c = Client()
        response = c.post('/logout/')
        self.assertEquals(response.status_code, 200)

    def test_user_can_open_registartion_page(self):
        c = Client()
        response = c.get('/register/')
        self.assertNotEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, 403)
        self.assertNotEquals(response.content, "")

    def test_user_can_register(self):
        c = Client()
        data = {'username': 'bob',
                'password1': 'asd123zxc456',
                'password2': 'asd123zxc456'
                }
        response = c.post('/register/', data)
        self.assertEquals(response.status_code, 302)
        user = User.objects.get(id=1)
        self.assertEquals(user.username, 'bob')

    def test_user_can_login(self):
        User.objects.create_user(username='test', password='test')
        c = Client()
        self.assertEquals(c.login(username = 'test', password = 'test'), True)
        response = c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_user_cant_login_if_not_have_account(self):
        c = Client()
        self.assertEquals(c.login(username = 'test', password = 'test'), False)
