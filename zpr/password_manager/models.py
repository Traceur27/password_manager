from django.db import models
from django.contrib.auth.models import User
from cryptopp import passwordXor
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64

# Create your models here.


class PasswordEntry(models.Model):
    """
    Klasa opisuje rekord zapamiętanego hasła
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.TextField()

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

        if algorithm == 'xor':
            # passwordXor zwraca base64
            self.password = passwordXor(self.password, master_password)

    def decrypt(self, master_password):
        """
        Odszyfrowuje pole password i zwraca hasło w postaci jawnej
        """
        algorithm = UserExtension.objects.get(
                user=self.user).encryption_algorithm

        decodedPass = base64.b64decode(self.password)
        if algorithm == 'xor':
            return base64.b64decode(passwordXor(decodedPass, master_password))
        return base64.b64decode(self.password)

    def __str__(self):
        return self.name


class UserExtension(models.Model):
    user = models.OneToOneField(User)
    ALGORITHMS = (("xor", "xor"), )
    encryption_algorithm = models.CharField(
        max_length=50, choices=ALGORITHMS, default='xor')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
