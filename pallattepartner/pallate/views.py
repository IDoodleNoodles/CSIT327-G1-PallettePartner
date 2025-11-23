from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User

from .forms import (
    RegisterForm,
    CollaborationForm,
    ProfileForm,
    ArtworkForm,
    MessageForm,
    ArtworkCommentForm,
)

from .models import (
    Collaboration,
    Message,
    Notification,
    Artwork,
    Favorite,
    ArtworkComment,
    Notification,
)
from pallattepartner.pallate import models

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
    # Collab posts
    posts = (
        Collaboration.objects
        .select_related('user')
        .order_by('-created_at')
    )

    # Artworks + number of comments per artwork
    artworks = (
        Artwork.objects
        .select_related('user')
        .annotate(comment_count=Count('comments'))
        .order_by('-created_at')
    )

    # Favorites of current user
    user_favorites = Favorite.objects.filter(
        user=request.user
    ).values_list('artwork_id', flat=True)

    # 🔔 Notifications for this user (top 10 newest)
    notifications = (
        Notification.objects
        .filter(user=request.user)
        .order_by('-created_at')[:10]
    )

    # Unread count (for the little dot / badge)
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

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
        'posts': posts,
        'artworks': artworks,
        'user_favorites': user_favorites,
        'notifications': notifications,
        'unread_count': unread_count,
    })

@login_required(login_url='pallate:login')
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    # mark as read
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    # asa ta mo-redirect after clicking
    redirect_url = request.GET.get('next') or notification.target_url
    if not redirect_url:
        redirect_url = reverse('pallate:dashboard')

    return redirect(redirect_url)

@login_required(login_url='pallate:login')
def notifications_list(request):
    notifications = (
        Notification.objects
        .filter(user=request.user)
        .select_related('actor')
        .order_by('-created_at')[:50]
    )
    return render(request, 'pallate/notifications_list.html', {
        'notifications': notifications,
    })

# Artist Profile (view another user's public profile)
@login_required(login_url='pallate:login')
def artist_profile(request, user_id=None):
    from django.contrib.auth.models import User
    target_user_id = user_id or request.GET.get('user')
    if not target_user_id:
        target_user = request.user
    else:
        target_user = get_object_or_404(User, pk=target_user_id)

    # Fetch related data
    artist_profile = getattr(target_user, 'profile', None)
    artworks = Artwork.objects.filter(user=target_user).order_by('-created_at')
    user_collaborations = Collaboration.objects.filter(user=target_user).order_by('-created_at')

    user_favorites = Favorite.objects.filter(user=request.user).values_list('artwork_id', flat=True)

    context = {
        'artist_user': target_user,
        'artist_profile': artist_profile,
        'artworks': artworks,
        'user_collaborations': user_collaborations,
        'user_favorites': user_favorites,
    }
    return render(request, 'pallate/artist_profile.html', context)

@xframe_options_exempt
@login_required(login_url='pallate:login')
def artwork_comments(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    comments = ArtworkComment.objects.filter(artwork=artwork).select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = ArtworkCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.artwork = artwork
            comment.user = request.user
            comment.save()
            return redirect('pallate:artwork_comments', artwork_id=artwork.id)
    else:
        form = ArtworkCommentForm()

    return render(request, 'pallate/artwork_comments.html', {
        'artwork': artwork,
        'comments': comments,
        'form': form,
    })



# Collaboration Detail
@login_required(login_url='pallate:login')
def collaboration_detail(request, pk=None):
    # Support legacy route without pk by showing latest or redirecting
    if pk is None:
        collab = Collaboration.objects.order_by('-created_at').first()
        if not collab:
            messages.info(request, 'No collaboration found yet.')
            return redirect('pallate:dashboard')
    else:
        collab = get_object_or_404(Collaboration, pk=pk)

    owner = collab.user
    owner_profile = getattr(owner, 'profile', None)
    context = {
        'collaboration': collab,
        'owner': owner,
        'owner_profile': owner_profile,
    }
    return render(request, 'pallate/collaboration_detail.html', context)


# Account Page
@login_required(login_url='pallate:login')
def account(request):
    return render(request, 'pallate/account.html')


# Profile Page (View Only)
@login_required
def profile_view(request):
    profile = request.user.profile
    user_artworks = Artwork.objects.filter(user=request.user).order_by('-created_at')
    user_collaborations = Collaboration.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pallate/profile.html', {
        'profile': profile,
        'user_artworks': user_artworks,
        'user_collaborations': user_collaborations
    })


# Edit Profile (Form-based)
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            # If password was changed, update the session to keep user logged in
            password = form.cleaned_data.get('password')
            if password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
            
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
    favorite_posts = Favorite.objects.filter(user=request.user).select_related('artwork')

    return render(request, 'pallate/favorites.html', {
        'favorite_posts': favorite_posts
    })

# Toggle Favorite
@login_required
def toggle_favorite(request, artwork_id):
    from django.http import JsonResponse
    
    artwork = get_object_or_404(Artwork, id=artwork_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, artwork=artwork)
    
    if not created:
        favorite.delete()
        favorited = False
        messages.info(request, "Removed from favorites.")
    else:
        favorited = True
        messages.success(request, "Added to favorites!")
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'favorited': favorited})
    
    return redirect('pallate:dashboard')


@login_required
def collab_messages(request, pk):
    collaboration = get_object_or_404(Collaboration, pk=pk)

    messages_qs = (
        Message.objects
        .filter(collaboration=collaboration)
        .select_related("sender")
        .order_by("timestamp")
    )

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.collaboration = collaboration
            message.sender = request.user
            message.save()

            if hasattr(models, "Notification") and request.user != collaboration.user:
                try:
                    Notification.objects.create(
                        user=collaboration.user,
                        actor=request.user,
                        notification_type="message",
                        message=f"New message from {request.user.username} in '{collaboration.title}'",
                        target_url=reverse("pallate:collab_messages", args=[pk]),
                    )
                except TypeError:
                    Notification.objects.create(
                        user=collaboration.user,
                        text=f"New message from {request.user.username} in '{collaboration.title}'"
                    )

            messages.success(request, "Message sent!")
            return redirect('pallate:collab_messages', pk=pk)
    else:
        form = MessageForm()

    participants = (
        User.objects
        .filter(message__collaboration=collaboration)
        .distinct()
    )

    return render(request, 'pallate/collab_messages.html', {
        'collaboration': collaboration,
        'messages': messages_qs,
        'participants': participants,
        'form': form,
    })