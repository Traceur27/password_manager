from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PasswordEntry

class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=30)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())


class PasswordEntryForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=120)
    class Meta:
        model = PasswordEntry
        fields = ["name", "username","password"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
