from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Landing Page
def landing(request):
    return render(request, 'pallate/index.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('pallate:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'pallate/login.html', {'form': form})


# Register View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('pallate:welcome')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'pallate/register.html', {'form': form})


# Dashboard (Protected)
@login_required(login_url='pallate:login')
def dashboard(request):
    return render(request, 'pallate/dashboard.html')


# Artist Profile (Protected)
@login_required(login_url='pallate:login')
def artist_profile(request):
    return render(request, 'pallate/artist_profile.html')


# Collaboration Detail (Protected)
@login_required(login_url='pallate:login')
def collaboration_detail(request):
    return render(request, 'pallate/collaboration_detail.html')


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('pallate:landing')


# Welcome Page after Registration
def welcome(request):
    return render(request, 'pallate/welcome.html')


# Account Page (Protected)
@login_required(login_url='pallate:login')
def account(request):
    return render(request, 'pallate/account.html')