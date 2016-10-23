from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PasswordEntryForm
from .models import PasswordEntry

from .forms import LoginForm
from . import forms
from django.contrib.auth import authenticate
from django.contrib import messages
from django import forms

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
        messages.success(request, 'Password added successfully.')
        return redirect(reverse('index'))

    context = {"form": form}
    return render(request, "add_password.html", context)


@login_required
def edit_password(request, id = None):
    instance = get_object_or_404(PasswordEntry, id=id)
    form = PasswordEntryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Password entry edited successfully.')
        return redirect(reverse("index"))

    context = {"form": form, "id":id}
    return render(request, "edit_password.html", context)


@login_required
def delete_password(request, id = None):
    if request.method == 'GET':
        context = {"id":id}
        return render(request, "delete_confirmation.html", context)

    a = request.POST.get('yes')
    b = request.POST.get('no')

    if request.method == 'POST' and request.POST.get('yes') is not None:
        instance = get_object_or_404(PasswordEntry, id=id)
        instance.delete()
        messages.success(request, "Item deleted")

    return redirect(reverse("index"))


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})

@login_required
def edit_profile(request):
    return render(request, "profile-edit.html", {"user": request.user})

