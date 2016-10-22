from django import forms

class RegisterFrom(forms.Form):
    login = forms.CharField(label='Login', max_length=30)
    password = forms.CharField(label='Password', max_length=20)
