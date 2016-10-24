from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import PasswordEntryForm
from .forms import UpdateProfileForm
from .models import PasswordEntry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

@login_required
def index(request):
    password_list = PasswordEntry.objects.filter(user=request.user)
    paginator = Paginator(password_list, 10) # Show 10 per page

    page = request.GET.get('page')
    try:
        passwords = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        passwords = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        passwords = paginator.page(paginator.num_pages)

    return render(request, "list.html", {"list": passwords})


def do_login(request):
    pass


def register(request):
    form = UserCreationForm(request.POST or None)
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
def edit_password(request, id=None):
    instance = get_object_or_404(PasswordEntry, id=id)
    form = PasswordEntryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Password entry edited successfully.')
        return redirect(reverse("index"))

    context = {"form": form, "id": id}
    return render(request, "edit_password.html", context)


@login_required
def delete_password(request, id=None):
    if request.method == 'GET':
        instance = get_object_or_404(PasswordEntry, id=id)
        context = {"id": id, "site": instance.site}
        return render(request, "delete_confirmation.html", context)

    if request.method == 'POST' and request.POST.get('yes') is not None:
        instance = get_object_or_404(PasswordEntry, id=id)
        instance.delete()
        messages.success(request, "Item deleted")

    return redirect(reverse("index"))


@login_required
def profile(request):
    password_count = PasswordEntry.objects.filter(user=request.user).count()
    return render(request, "profile.html",
                  {"user": request.user, "count": password_count})


@login_required
def edit_profile(request):
    form = UpdateProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile save successfully")
            return redirect(reverse('profile'))
    return render(request, "profile-edit.html", {"form": form})
