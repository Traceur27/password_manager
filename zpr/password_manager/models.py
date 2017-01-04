from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64
from django.utils.translation import ugettext_lazy as _
import password_manager.util as pmutil


# Create your models here.


class PasswordEntry(models.Model):
    """
    Klasa opisuje rekord zapamiętanego hasła
    W bazie zapisane jest hasło zaszyfrowanie odpowiednim algorytmem
    ma ono postać napisu zakodowanego base64

    szyfrowanie:
    base64_encode(encrypt(password))
    deszyfrowanie
    decrypt(base64_decode(password))
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=120)
    username = models.CharField(_("Username"), max_length=120)
    password = models.TextField(_("Password"))

    def save(self, *args, **kwargs):
        """
        Zapis do bazy automatycznie szyfruje hasło
        """
        self.encrypt(kwargs['master'])
        super(PasswordEntry, self).save(*args)

    def rehash(self, old_password, new_password):
        """
        Funkcja zmienia klucz szyfujący hasło
        """
        self.decrypt_in_place(old_password)
        self.save(master=new_password)

    def encrypt(self, master_password):
        """
        Szyfruje pole password i zapisuje w nim ciąg base64
        Pole password powinno być zapisane w postaci jawnej przed wywołaniem
        tej metody
        """
        algorithm = UserExtension.objects.get(
            user=self.user).encryption_algorithm

        encryptor = pmutil.get_crypto_object(algorithm, master_password)
        self.password = encryptor.encrypt(self.password)

    def decrypt(self, master_password):
        """
        Odszyfrowuje pole password i zwraca hasło w postaci jawnej
        """
        algorithm = UserExtension.objects.get(
            user=self.user).encryption_algorithm

        encryptor = pmutil.get_crypto_object(algorithm, master_password)

        return encryptor.decrypt(self.password)

    def decrypt_in_place(self, master_password):
        """
        Odszyfrowuje pole password i ustawia je na postać jawną

        Uwaga:
        Dwukrotne użycie rzuca wyjątek związany z kodowaniem base64
        """

        self.password = self.decrypt(master_password)

    def __str__(self):
        return self.name


class UserExtension(models.Model):
    """
    Model przchowuje informacje o algorytmie szyfrowania wybranym przez
    użytkownika
    """
    user = models.OneToOneField(User)
    ALGORITHMS = pmutil.get_all_algorithms_choices()
    encryption_algorithm = models.CharField(
        _("Algorithm"),
        max_length=50, choices=ALGORITHMS, default='xor')

    def algorithm_changed(self):
        """
        Sprawdza czy algorytm szyfrowania się zmienił od czasu pobrania z bazy
        i hasła wymagają ponownego zaszyfrowania
        """
        try:
            from_db = UserExtension.objects.get(id=self.id)
            return from_db.encryption_algorithm != self.encryption_algorithm
        except UserExtension.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        """
        :Keyword Arguments:
            * *master* - główne hasło szyfrujące hasła użytkownika
        """
        # usuwamy argument bo klasa bazowa nie spodziewa się go w kwargs
        try:
            master_password = kwargs.pop('master')
        except KeyError:
            raise ValueError(
                "Cant rehash passwords if argument 'master' is missing")
        # sprawdzamy czy obiekt się zmienił aby niepotrzebnie nie przeliczać
        # nowych zaszyfrowanych haseł zawsze gdy zapisujemy
        if self.algorithm_changed():
            # zachowaj kopię starych haseł zaszyfrowanych poprzednim algorytmem
            old_passwords = PasswordEntry.objects.filter(user=self.user)
            for p in old_passwords:
                # odszyfruj je
                p.decrypt_in_place(master_password)
            # zapisz informację o nowym algorymie w bazie
            super(UserExtension, self).save(*args, **kwargs)
            # zaszyfruj wszystkie hasła nowym algorytmem i zapisz je w bazie
            for p in old_passwords:
                p.save(master=master_password)
        else:
            # Algorytm się nie zmienił
            super(UserExtension, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
