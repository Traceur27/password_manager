from django.db import models

# Create your models here.


class PasswordEntry(models.Model):
    site = models.CharField(max_length=120)
    password = models.TextField()

    def __str__(self):
        return self.site
