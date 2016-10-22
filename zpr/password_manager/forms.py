from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=30)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())
