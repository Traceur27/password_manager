from django.db import models
from django.contrib.auth.models import User
from cryptopp import passwordXor
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.TextField()

    def save(self, *args, **kwargs):
        algorithm = UserExtension.objects.get(user=self.user).encryption_algorithm
        if algorithm == 'xor':
            self.password = passwordXor(self.password, kwargs['master'])
        super(PasswordEntry, self).save(*args)

    def __str__(self):
        return self.name



class UserExtension(models.Model):
    user = models.OneToOneField(User)
    ALGORITHMS = (
            ("xor", "xor"),
            )
    encryption_algorithm = models.CharField(max_length=50, choices=ALGORITHMS,
                                            default='xor')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
