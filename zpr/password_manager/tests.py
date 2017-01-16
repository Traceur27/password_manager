from django.test import TestCase, Client
from django.contrib.auth.models import User
from password_manager.models import PasswordEntry, UserExtension
from password_manager.util import get_crypto_object

#Kody statusu Http
REDIRECT_302 = 302
OK_200 = 200
NOT_FOUND_404 = 404
FORBIDDEN_403 = 403

DEFAULT_ID_FOR_ONE_ENTRY = 1

INDEX_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
REGISTER_URL = '/register/'
ME_URL = '/me/'
ME_REMOVE_URL = '/me/remove/'
ME_EDIT_URL = '/me/edit/'
ME_CHANGE_PASSWORD_URL = '/me/change-password/'
ME_CHANGE_PASSWORD_DONE_URL = '/me/change-password-done/'
ADD_PASSWORD_URL = '/add-password/'
EDIT_PASSWORD_URL = '/edit-password/'
DELETE_PASSWORD_URL = '/delete-password/'


class PasswordManagerTests(TestCase):

    # Utwórz i zaloguj uzytkownika
    def get_logged_in_client(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        data = {"username": "test", "password": "test"}
        c.post(LOGIN_URL, data)
        return c

    def test_not_logged_in_user_cant_open_restricted_access_pages(self):
        # W każdym przypadku użytkownik powinien zostać przekierowany do logowania
        c = Client()
        response = c.get(INDEX_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(ME_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(ME_EDIT_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(ME_CHANGE_PASSWORD_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(ME_CHANGE_PASSWORD_DONE_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(ADD_PASSWORD_URL)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(EDIT_PASSWORD_URL + '1')
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(DELETE_PASSWORD_URL + '1')
        self.assertEquals(response.status_code, REDIRECT_302)

    def test_user_can_add_password(self):
        c = self.get_logged_in_client()
        # Utwórz obiekt w bazie danych
        data = {}
        response = c.post(ADD_PASSWORD_URL, data)
        passwords = PasswordEntry.objects.all()
        # Forma nie została wypełniona - hasło nie dodane
        self.assertEqual(len(passwords), 0)
        self.assertEquals(response.status_code, OK_200)
        data = {"name": "asd", "username": "asd1", "password": "asdPass"}
        response = c.post(ADD_PASSWORD_URL, data)
        passwords = PasswordEntry.objects.all()
        self.assertEqual(len(passwords), 1)
        # Hasło dodane - przekierowanie do listy
        self.assertEquals(response.status_code, REDIRECT_302)

    def test_user_can_edit_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test') # Zapis hasła w bazie

        data = {}
        response = c.post(EDIT_PASSWORD_URL + psw.id.__str__(), data)
        self.assertEquals(response.status_code, OK_200)
        psw = PasswordEntry.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        self.assertEquals(psw.decrypt('test'), 'pass123')

        data = {"name": "test1", "username": "us", "password": "new_pass"}
        response = c.post(EDIT_PASSWORD_URL + psw.id.__str__(), data)
        self.assertEquals(response.status_code, REDIRECT_302)
        psw = PasswordEntry.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        self.assertEquals(psw.decrypt('test'), 'new_pass')

    def test_user_can_delete_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        data = {"answer": "yes"}
        response = c.get(DELETE_PASSWORD_URL + (psw.id + 1).__str__())
        self.assertEquals(response.status_code, NOT_FOUND_404)
        response = c.get(DELETE_PASSWORD_URL + psw.id.__str__())
        self.assertEquals(response.status_code, OK_200)
        response = c.post(DELETE_PASSWORD_URL + psw.id.__str__(), data)
        self.assertEquals(response.status_code, REDIRECT_302)
        response = c.get(DELETE_PASSWORD_URL + psw.id.__str__())
        self.assertEquals(response.status_code, NOT_FOUND_404)

    def test_user_can_list_passwords(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        response = c.get(INDEX_URL)
        self.assertEquals(response.status_code, OK_200)
        response = c.get("/?filter=test&page=1")
        self.assertEquals(response.status_code, OK_200)
        response = c.get("/?filter=test&page=9999")
        self.assertEquals(response.status_code, OK_200)

    def test_user_can_change_master_password(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        old_password = us.password
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        data = {'old_password': 'test',
                'new_password1': 'ASDasd123',
                'new_password2': 'ASDasd123'
                }
        response = c.get(ME_CHANGE_PASSWORD_URL)
        response = c.post(ME_CHANGE_PASSWORD_URL, data)
        self.assertEquals(response.status_code, REDIRECT_302)
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        self.assertNotEquals(old_password, us.password)

    def test_user_can_logout(self):
        User.objects.create_user(username='test', password='test')
        self.assertEquals(self.client.login(username='test', password='test'), True)
        c = Client()
        response = c.post(LOGOUT_URL)
        self.assertEquals(response.status_code, OK_200)

    def test_user_can_open_registartion_page(self):
        c = Client()
        response = c.get(REGISTER_URL)
        self.assertNotEquals(response.status_code, NOT_FOUND_404)
        self.assertNotEquals(response.status_code, FORBIDDEN_403)
        self.assertNotEquals(response.content, "")

    def test_user_can_register(self):
        c = Client()
        data = {'username': 'bob',
                'password1': 'asd123zxc456',
                'password2': 'asd123zxc456'
                }
        response = c.post(REGISTER_URL, data)
        self.assertEquals(response.status_code, REDIRECT_302)
        user = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        self.assertEquals(user.username, 'bob')

    def test_user_can_login(self):
        c = Client()
        User.objects.create_user(username='test', password='test')

        data = {"username": "test", "password": "test123"}
        c.post(LOGIN_URL, data)
        response = c.get(INDEX_URL)
        self.assertEquals(response.status_code, REDIRECT_302)

        c = Client()
        data = {"username": "test", "password": "test"}
        c.post(LOGIN_URL, data)
        response = c.get(INDEX_URL)
        self.assertEquals(response.status_code, OK_200)

    def test_user_cant_login_if_not_have_account(self):
        c = Client()
        self.assertEquals(c.login(username = 'test', password = 'test'), False)

    def test_logged_in_user_can_disply_profile(self):
        c = self.get_logged_in_client()
        response = c.get(ME_URL)
        self.assertEqual(response.status_code, OK_200)

    def test_logged_in_user_can_edit_profile(self):
        c = self.get_logged_in_client()
        us = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        psw = PasswordEntry(user=us, name='test1', username='us', password='pass123')
        psw.save(master='test')
        c.get(ME_EDIT_URL)
        response = c.post('/me/edit/',
                {'username': "test",
            "email": "user@example.com",
            "first_name": "test",
            "last_name": "test",
            "encryption_algorithm": "plain"})
        user = User.objects.get(id=DEFAULT_ID_FOR_ONE_ENTRY)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.first_name, "test")
        user_extension = UserExtension.objects.get(user=user)
        self.assertEqual(user_extension.encryption_algorithm, "plain")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_user_can_remove_account(self):
        c = self.get_logged_in_client()

        c.get(ME_REMOVE_URL)
        response = c.post(ME_REMOVE_URL, {"password": "test123"})
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(UserExtension.objects.all()), 1)
        response = c.post(ME_REMOVE_URL, {"password": "test"})
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(UserExtension.objects.all()), 0)


class CryptoCppTests(TestCase):
    def test_plain(self):
        plain = get_crypto_object('plain', 'secret')
        message = "Test"
        encrypted_message = plain.encrypt(message)
        self.assertEquals(encrypted_message, 'VGVzdA==')
        decrypted_mesage = plain.decrypt(encrypted_message)
        self.assertEquals(message, decrypted_mesage)

    def test_xor(self):
        plain = get_crypto_object('xor', 'secret')
        message = "Test"
        encrypted_message = plain.encrypt(message)
        self.assertEquals(encrypted_message, 'JwAQBg==')
        decrypted_mesage = plain.decrypt(encrypted_message)
        self.assertEquals(message, decrypted_mesage)

    def test_rc4(self):
        plain = get_crypto_object('rc4', 'secret')
        message = "Test"
        encrypted_message = plain.encrypt(message)
        self.assertEquals(encrypted_message, 'uVOhaA==')
        decrypted_mesage = plain.decrypt(encrypted_message)
        self.assertEquals(message, decrypted_mesage)
