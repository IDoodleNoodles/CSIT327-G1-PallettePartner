from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CollaborationForm
from .models import Collaboration
from .models import Collaboration, Message, Notification
from .models import Collaboration, Message


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
    posts = Collaboration.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, "Collaboration post created successfully!")
            return redirect('pallate:dashboard')
    else:
        form = CollaborationForm()

    return render(request, 'pallate/dashboard.html', {
        'form': form,
        'posts': posts
    })


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
    return redirect('pallate:login')


# Welcome Page after Registration
def welcome(request):
    return render(request, 'pallate/welcome.html')


# Account Page (Protected)
@login_required(login_url='pallate:login')
def account(request):
    return render(request, 'pallate/account.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.art_type = request.POST.get('art_type')
        profile.portfolio = request.POST.get('portfolio')
        profile.bio = request.POST.get('bio')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        return redirect('pallate:profile')
    return render(request, 'pallate/profile.html', {'profile': profile})

@login_required
def collab_messages(request, pk):
    collaboration = get_object_or_404(Collaboration, pk=pk)
    messages_qs = Message.objects.filter(collaboration=collaboration).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            # Create the message
            new_message = Message.objects.create(
                collaboration=collaboration,
                sender=request.user,
                text=text
            )
            # (but only if the sender isn’t the owner)
            if request.user != collaboration.user:
                Notification.objects.create(
                    user=collaboration.user,
                    text=f"New message from {request.user.username} in '{collaboration.title}'"
                )

            return redirect('pallate:collab_messages', pk=pk)

    return render(request, 'pallate/collab_messages.html', {
        'collaboration': collaboration,
        'messages': messages_qs
    })