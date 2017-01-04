from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
from password_manager.models import PasswordEntry, UserExtension


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
        self.assertEquals(response.status_code, 302)
        response = c.get('/delete-password/1')
        self.assertEquals(response.status_code, 302)

    def test_user_can_add_password(self):
        c = self.get_logged_in_client()
        # utwórz obiekt w bazie danych
        data = {}
        response = c.post('/add-password/', data)
        passwords = PasswordEntry.objects.all()
        self.assertEqual(len(passwords), 0)
        self.assertEquals(response.status_code, 200)
        data = {"name": "asd", "username": "asd1", "password": "asdPass"}
        response = c.post('/add-password/', data)
        passwords = PasswordEntry.objects.all()
        self.assertEqual(len(passwords), 1)
        self.assertEquals(response.status_code, 302)

    def test_user_can_edit_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')

        data = {}
        response = c.post('/edit-password/' + psw.id.__str__(), data)
        self.assertEquals(response.status_code, 200)
        psw = PasswordEntry.objects.get(id=1)
        self.assertEquals(psw.decrypt('test'), b'pass123')


        data = {"name":"test1", "username":"us", "password":"new_pass"}
        response = c.post('/edit-password/' + psw.id.__str__(), data)
        self.assertEquals(response.status_code, 302)
        psw = PasswordEntry.objects.get(id=1)
        self.assertEquals(psw.decrypt('test'), b'new_pass')

    def test_user_can_delete_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        data = {"answer":"yes"}
        response = c.get('/delete-password/' + (psw.id + 1).__str__())
        self.assertEquals(response.status_code, 404)
        response = c.get('/delete-password/' + psw.id.__str__())
        self.assertEquals(response.status_code, 200)
        response = c.post('/delete-password/' + psw.id.__str__(), data)
        self.assertEquals(response.status_code, 302)
        response = c.get('/delete-password/' + psw.id.__str__())
        self.assertEquals(response.status_code, 404)

    def test_user_can_list_passwords(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        response = c.get("/")
        self.assertEquals(response.status_code, 200)
        response = c.get("/?filter=test&page=1")
        self.assertEquals(response.status_code, 200)
        response = c.get("/?filter=test&page=9999")
        self.assertEquals(response.status_code, 200)

    def test_user_can_change_master_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        old_password = us.password
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        data = {'old_password': 'test',
                'new_password1': 'ASDasd123',
                'new_password2': 'ASDasd123'
                }
        response = c.get('/me/change-password/')
        response = c.post('/me/change-password/', data)
        self.assertEquals(response.status_code, 302)
        us = User.objects.get(id=1)
        self.assertNotEquals(old_password, us.password)

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
        c = Client()
        User.objects.create_user(username='test', password='test')

        data = {"username": "test", "password": "test123"}
        c.post('/login/', data)
        response = c.get("/")
        self.assertEquals(response.status_code, 302)

        c = Client()
        data = {"username": "test", "password": "test"}
        c.post('/login/', data)
        response = c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_user_cant_login_if_not_have_account(self):
        c = Client()
        self.assertEquals(c.login(username = 'test', password = 'test'), False)

    def test_logged_in_user_can_disply_profile(self):
        c = self.get_logged_in_client()
        response = c.get('/me/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_edit_profile(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=1)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        c.get('/me/edit/')
        response = c.post('/me/edit/',
                {'username': "test",
            "email": "user@example.com",
            "first_name": "test",
            "last_name": "test",
            "encryption_algorithm": "plain"})
        user = User.objects.get(id=1)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.first_name, "test")
        user_extension = UserExtension.objects.get(user=user)
        self.assertEqual(user_extension.encryption_algorithm, "plain")
        self.assertEqual(response.status_code, 302)

    def test_user_can_remove_account(self):
        c = self.get_logged_in_client()

        c.get('/me/remove/')
        response = c.post('/me/remove/', {"password": "test123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(UserExtension.objects.all()), 1)
        response = c.post('/me/remove/', {"password": "test"})
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(UserExtension.objects.all()), 0)
