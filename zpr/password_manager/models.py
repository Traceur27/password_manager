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
        Funkcja zmienia klucz szyfujący hasła
        """
        self.password = self.decrypt(old_password)
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
        Dwukrotne użycie rzuca wyjątek
        """

        self.password = self.decrypt(master_password)

    def __str__(self):
        return self.name


class UserExtension(models.Model):
    user = models.OneToOneField(User)
    ALGORITHMS = (
            ("plain", "Plain"),
            ("xor", "XOR by key"),
            ('rc4', 'RC4')
            )
    encryption_algorithm = models.CharField(_("Algorithm"),
        max_length=50, choices=ALGORITHMS, default='xor')

    def dirty(self):
        """
        Sprawdza czy obiekt się zmienił o czasu pobrania z bazy
        """
        from_db = UserExtension.objects.get(id=self.id)
        return from_db.encryption_algorithm != self.encryption_algorithm

    def save(self, *args, **kwargs):
        # sprawdzamy czy obiekt się zmienił aby niepotrzebnie nie przeliczać
        # nowych zaszyfrowanych haseł
        if self.dirty():
            # zachowaj kopię starych haseł zaszyfrowanych poprzednim algorytmem
            old_passwords = PasswordEntry.objects.all()
            for p in old_passwords:
                # odszyfruj je
                p.decrypt_in_place(kwargs['master'])
            # zapisz informację o nowym algorymie w bazie
            super(UserExtension, self).save(*args)
            # zaszyfruj wszystkie hasła nowym algorymem
            for p in old_passwords:
                p.save(master=kwargs['master'])
        else:
            super(UserExtension, self).save(*args)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
