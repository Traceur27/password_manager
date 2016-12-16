from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import PasswordEntryForm
from .forms import UpdateProfileForm
from .forms import RemoveAccountForm
from .forms import UpdateAlgorithmForm
from .models import PasswordEntry, UserExtension
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.db.models import Q


# Create your views here.

@login_required
def index(request):
    query = Q(user=request.user)
    filter_query = request.GET.get('filter','')
    print (filter_query)
    query=None
    if filter_query:
        query = Q(name__icontains=filter_query) | Q(username__icontains=filter_query)
        password_list = PasswordEntry.objects.filter(query, user=request.user)
    else:
        password_list = PasswordEntry.objects.filter(user=request.user)
    paginator = Paginator(password_list, 10)  # Show 10 per page

    page = request.GET.get('page')
    try:
        passwords = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        passwords = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        passwords = paginator.page(paginator.num_pages)

    return render(request, "list.html", {"list": passwords, "query": filter_query})


def do_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.user_cache)
        request.session['master'] = form.cleaned_data.get('password')
        return redirect(reverse('index'))
    return render(request, "registration/login.html", {"form": form})


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
        instance.save(master=request.session['master'])
        messages.success(request, 'Password added successfully.')
        return redirect(reverse('index'))

    context = {"form": form}
    return render(request, "add_password.html", context)


@login_required
def edit_password(request, id=None):
    instance = get_object_or_404(PasswordEntry, id=id)
    form = PasswordEntryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save(master=request.session['master'])
        messages.success(request, 'Password entry edited successfully.')
        return redirect(reverse("index"))

    context = {"form": form, "id": id}
    return render(request, "edit_password.html", context)


@login_required
def delete_password(request, id=None):
    if request.method == 'GET':
        instance = get_object_or_404(PasswordEntry, id=id)
        context = {"id": id, "name": instance.name }
        return render(request, "delete_confirmation.html", context)

    if request.method == 'POST' and request.POST.get('yes', ''):
        instance = get_object_or_404(PasswordEntry, id=id)
        instance.delete()
        messages.success(request, "Password entry deleted")

    return redirect(reverse("index"))


@login_required
def profile(request):
    password_count = PasswordEntry.objects.filter(user=request.user).count()
    return render(request, "profile.html",
                  {"user": request.user, "count": password_count})


@login_required
def edit_profile(request):
    update_profile_form = UpdateProfileForm(request.POST or None,
            instance=request.user)
    change_algorithm_form = UpdateAlgorithmForm(request.POST or None,
            instance=UserExtension.objects.get(user=request.user))
    if request.method == "POST":
        if update_profile_form.is_valid():
            update_profile_form.save()
            if change_algorithm_form.is_valid():
                instance = change_algorithm_form.save(commit=False)
                instance.save(master=request.session['master'])
            messages.success(request, "Profile saved successfully")
            return redirect(reverse('profile'))
    return render(request, "profile-edit.html", {"pform": update_profile_form,
        "aform": change_algorithm_form})



@login_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        passwords = PasswordEntry.objects.filter(user=request.user)
        for p in passwords:
            p.rehash(form.cleaned_data.get('old_password'),
                     form.cleaned_data.get('new_password1'))
        request.session['master'] = form.cleaned_data.get('new_password1')
        messages.success(request, "Master password change successfully")
        return redirect(reverse('profile'))
    return render(request, "registration/password_change_form.html",
                  {"form": form})


@login_required
def remove_account(request):
    form = RemoveAccountForm(request.user, request.POST or None)
    if form.is_valid():
        logout(request)
        form.save()
        return redirect(reverse('login'))
    return render(request,
            "confirm_remove_account.html",
            {"form": form})

