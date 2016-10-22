from django.contrib.auth.views import login
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginForm
from . import forms
from django.contrib.auth import authenticate


# Create your views here.

def index(request):
    return HttpResponse("todo")

def do_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("index"))

    return redirect(reverse('login'))


def register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))

    return render(request, "register.html", {"form":form})


