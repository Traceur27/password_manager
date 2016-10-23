from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PasswordEntryForm
from .models import PasswordEntry

from .forms import LoginForm
from . import forms
from django.contrib.auth import authenticate

# Create your views here.

@login_required
def index(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, "list.html", {"list":passwords})

def do_login(request):
    pass

def register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))

    return render(request, "registration/register.html", {"form": form})


@login_required
def add_password_entry(request):
    form = PasswordEntryForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect(reverse("index"))

    context = {"form": form}
    return render(request, "password_manager_form.html", context)
