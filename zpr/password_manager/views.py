from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate
from . import forms


# Create your views here.

def index(request):
    return HttpResponse("todo")

def login(request):
    if request.user.is_authenticated:
        redirect(reverse('index'))
    user = authenticate(username='john', password='secret')

def register(request):
    form = forms.RegisterFrom()
    return render(request, "register.html", {"form":form})

