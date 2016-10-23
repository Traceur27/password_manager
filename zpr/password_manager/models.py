from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PasswordEntry(models.Model):
    user = models.ForeignKey(User)
    site = models.CharField(max_length=120)
    password = models.TextField()

    def __str__(self):
        return self.site
