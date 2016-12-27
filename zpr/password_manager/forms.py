from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import PasswordEntry, UserExtension


class LoginForm(forms.Form):
    login = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(
            label=_("Password"),
            max_length=20,
            widget=forms.PasswordInput())


class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordEntry
        fields = ["name", "username", "password"]
        widgets = {
                "password": forms.PasswordInput(),
                }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateAlgorithmForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ['encryption_algorithm']


class RemoveAccountForm(forms.Form):
    password = forms.CharField(
            label=_("Password"),
            max_length=20,
            widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RemoveAccountForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        form_pw = self.cleaned_data["password"]
        if not self.user.check_password(form_pw):
            raise forms.ValidationError("Password is invalid")
        return form_pw

    def save(self):
        self.user.delete()

