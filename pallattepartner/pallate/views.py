from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request, 'pallate/index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pallate:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'pallate/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('pallate:welcome')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'pallate/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'pallate/dashboard.html')


@login_required
def artist_profile(request):
    return render(request, "pallate/artist_profile.html")


@login_required
def collaboration_detail(request):
    return render(request, "pallate/collaboration_detail.html")


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('pallate:landing')


def welcome(request):
    return render(request, 'pallate/welcome.html')


@login_required
def account(request):
    return render(request, 'pallate/account.html')