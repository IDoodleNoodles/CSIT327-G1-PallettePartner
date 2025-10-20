from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CollaborationForm, ProfileForm, ArtworkForm, CommentForm
from .models import Collaboration, Message, Notification, Artwork, Favorite, Comment




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


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('pallate:login')


# Welcome Page
def welcome(request):
    return render(request, 'pallate/welcome.html')


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


# Artist Profile
@login_required(login_url='pallate:login')
def artist_profile(request):
    return render(request, 'pallate/artist_profile.html')


# Collaboration Detail
@login_required(login_url='pallate:login')
def collaboration_detail(request):
    return render(request, 'pallate/collaboration_detail.html')


# Account Page
@login_required(login_url='pallate:login')
def account(request):
    return render(request, 'pallate/account.html')


# Profile Page (View & Edit)
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
        messages.success(request, "Profile updated successfully!")
        return redirect('pallate:profile')
    return render(request, 'pallate/profile.html', {'profile': profile})


# Edit Profile (Form-based)
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('pallate:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'pallate/edit_profile.html', {'form': form})


# Upload Artwork
@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = request.user
            artwork.save()
            messages.success(request, "Artwork uploaded successfully!")
            return redirect('pallate:dashboard')
    else:
        form = ArtworkForm()
    return render(request, 'pallate/upload_artwork.html', {'form': form})


# Favorites Page
@login_required
def favorites(request):
    favorite_posts = Favorite.objects.filter(user=request.user).select_related('collaboration')

    return render(request, 'pallate/favorites.html', {
        'favorite_posts': favorite_posts
    })

# Toggle Favorite
@login_required
def toggle_favorite(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, artwork=artwork)
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites!")
    return redirect('pallate:dashboard')


# Collaboration Chat
@login_required
def collab_messages(request, pk):
    collaboration = get_object_or_404(Collaboration, pk=pk)
    messages_qs = Message.objects.filter(collaboration=collaboration).order_by('timestamp')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = collaboration
            comment.user = request.user
            comment.save()

            # Notify the owner
            if request.user != collaboration.user:
                Notification.objects.create(
                    user=collaboration.user,
                    text=f"New message from {request.user.username} in '{collaboration.title}'"
                )

            return redirect('pallate:collab_messages', pk=pk)

    return render(request, 'pallate/collab_messages.html', {
        'collaboration': collaboration,
        'messages': messages_qs,
        'form': form
    })