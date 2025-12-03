from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.models import User

from .forms import (
    RegisterForm,
    CollaborationForm,
    ProfileForm,
    ArtworkForm,
    MessageForm,
    ArtworkCommentForm,
    CollaborationFeedbackForm,
    PasswordResetRequestForm,
    SecurityQuestionAnswerForm,
    NewPasswordForm,
)

from .models import (
    Collaboration,
    Message,
    Notification,
    Artwork,
    Favorite,
    ArtworkComment,
    Notification,
    CollaborationFeedback,
    CollaborationMatch,
    Profile,
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
            return redirect('pallate:dashboard')
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
    # Get selected categories from query params
    selected_categories = request.GET.getlist('categories')
    
    # Collab posts
    posts = (
        Collaboration.objects
        .select_related('owner')
        .order_by('-created_at')
    )

    # Artworks + number of comments per artwork
    artworks_queryset = (
        Artwork.objects
        .select_related('user')
        .annotate(comment_count=Count('comments'))
        .order_by('-created_at')
    )
    
    # Filter artworks by categories if specified
    if selected_categories:
        # Create a Q object for OR filtering across categories
        category_filter = Q()
        for category in selected_categories:
            category_filter |= Q(categories__icontains=category)
        artworks_queryset = artworks_queryset.filter(category_filter)
    
    artworks = artworks_queryset

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

    # Define default categories
    default_categories = [
        'Digital Art', 'Traditional Art', 'Photography', 
        'Illustration', 'Graphic Design', '3D Art', 
        'Animation', 'Concept Art'
    ]
    
    # Get all unique categories from artworks
    all_artworks = Artwork.objects.all()
    all_categories = set()
    for artwork in all_artworks:
        categories_list = artwork.get_categories_list()
        all_categories.update(categories_list)
    
    # Combine artwork categories with default categories
    # This ensures we always have categories to display
    all_categories = sorted(list(set(list(all_categories) + default_categories)))

    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
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
        'all_categories': all_categories,
        'selected_categories': selected_categories,
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
    """Discover Artists page - shows all artists with their recent work"""
    from django.contrib.auth.models import User
    from django.db.models import Count, Prefetch
    
    # Get all users with their profiles and recent artworks
    artists = User.objects.select_related('profile').prefetch_related(
        Prefetch('artworks', queryset=Artwork.objects.order_by('-created_at')[:3], to_attr='recent_artworks')
    ).annotate(
        artwork_count=Count('artworks'),
        collab_count=Count('owned_collaborations')
    ).filter(is_active=True).order_by('-date_joined')
    
    # If user_id is provided, show that specific artist
    if user_id:
        target_user = get_object_or_404(User, pk=user_id)
        artist_profile = getattr(target_user, 'profile', None)
        artworks = Artwork.objects.filter(user=target_user).order_by('-created_at')
        user_collaborations = Collaboration.objects.filter(owner=target_user).order_by('-created_at')
        user_favorites = Favorite.objects.filter(user=request.user).values_list('artwork_id', flat=True)
        
        context = {
            'artist_user': target_user,
            'artist_profile': artist_profile,
            'artworks': artworks,
            'user_collaborations': user_collaborations,
            'user_favorites': user_favorites,
            'show_single': True,
        }
        return render(request, 'pallate/artist_profile.html', context)
    
    # Show all artists (discover mode)
    context = {
        'artists': artists,
        'show_single': False,
    }
    return render(request, 'pallate/artist_profile.html', context)

# API endpoint to fetch artworks by category
@login_required(login_url='pallate:login')
def fetch_artworks_by_category(request):
    from django.http import JsonResponse
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle multiple categories
        categories = request.GET.get('categories', '')
        
        if categories:
            # Split categories by comma
            category_list = [cat.strip() for cat in categories.split(',') if cat.strip()]
            
            # Create a Q object for OR filtering across categories
            from django.db.models import Q
            category_filter = Q()
            for category in category_list:
                category_filter |= Q(categories__icontains=category)
            
            artworks = Artwork.objects.filter(category_filter).select_related('user').annotate(
                comment_count=Count('comments')
            ).order_by('-created_at')[:20]  # Limit to 20 artworks
        else:
            artworks = Artwork.objects.select_related('user').annotate(
                comment_count=Count('comments')
            ).order_by('-created_at')[:20]
        
        # Serialize artworks data
        artworks_data = []
        for artwork in artworks:
            artworks_data.append({
                'id': artwork.id,
                'title': artwork.title,
                'description': artwork.description,
                'image_url': artwork.image.url if artwork.image else '',
                'user_username': artwork.user.username,
                'user_first_name': artwork.user.first_name,
                'user_id': artwork.user.id,
                'created_at': artwork.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'comment_count': artwork.comment_count,
                'favorite_count': artwork.favorited_by.count(),
                'categories': artwork.get_categories_list(),
            })
        
        return JsonResponse({'artworks': artworks_data})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
    
    # Get all collaboration opportunities excluding the current one
    all_posts = Collaboration.objects.select_related('owner').exclude(pk=collab.pk).order_by('-created_at')
    
    # Get roles for this collaboration
    roles = collab.roles.select_related('filled_by').all()
    
    context = {
        'collaboration': collab,
        'owner': owner,
        'owner_profile': owner_profile,
        'all_posts': all_posts,
        'roles': roles,
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
    user_collaborations = Collaboration.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'pallate/profile.html', {
        'profile': profile,
        'user_artworks': user_artworks,
        'user_collaborations': user_collaborations
    })


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save Profile + User (username, email, names, password)
            profile_instance = form.save(commit=True)

            # Hash security answer if provided
            security_answer = form.cleaned_data.get('security_answer')
            if security_answer:
                profile_instance.security_answer = make_password(security_answer)
                profile_instance.save(update_fields=['security_answer'])

            # Keep user logged in if password changed
            password = form.cleaned_data.get('password')
            if password:
                update_session_auth_hash(request, request.user)

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
            
            # Handle categories - setting both category and categories fields for database compatibility
            selected_categories = request.POST.get('selected_categories', '')
            if selected_categories:
                artwork.categories = selected_categories
                # Also set the category field if it exists in the database schema
                if hasattr(artwork, 'category'):
                    artwork.category = selected_categories.split(',')[0]  # Use first category as the singular category
            else:
                # Set default category if none selected
                artwork.categories = 'Digital Art'
                # Also set the category field if it exists in the database schema
                if hasattr(artwork, 'category'):
                    artwork.category = 'Digital Art'
            
            artwork.save()
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
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'favorited': favorited})
    
    return redirect('pallate:dashboard')


# Search View
@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    
    artworks = []
    artists = []
    
    if query:
        # Search artworks by title or description
        artworks = (
            Artwork.objects
            .filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
            .select_related('user')
            .annotate(comment_count=Count('comments'))
            .order_by('-created_at')
        )
        
        # Search users by username or profile details
        artists = (
            User.objects
            .filter(
                Q(username__icontains=query) |
                Q(profile__bio__icontains=query) |
                Q(profile__art_type__icontains=query)
            )
            .select_related('profile')
            .distinct()
        )
    
    # Get user's favorites for the heart icon display
    user_favorites = Favorite.objects.filter(
        user=request.user
    ).values_list('artwork_id', flat=True)
    
    return render(request, 'pallate/search_results.html', {
        'query': query,
        'artworks': artworks,
        'artists': artists,
        'user_favorites': user_favorites,
    })


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


# ============================================
# NEW FEATURES: Matching, Feedback, Featured
# ============================================

@login_required
def find_collaborators(request):
    """Find and suggest potential collaborators based on art_type and interests"""
    current_profile = request.user.profile
    
    # Get all users except current user
    potential_matches = []
    all_users = User.objects.exclude(id=request.user.id).select_related('profile')
    
    for user in all_users:
        if hasattr(user, 'profile'):
            profile = user.profile
            match_score = 0
            match_reasons = []
            
            # Check art_type match
            if current_profile.art_type and profile.art_type:
                if current_profile.art_type.lower() in profile.art_type.lower() or \
                   profile.art_type.lower() in current_profile.art_type.lower():
                    match_score += 50
                    match_reasons.append(f"Matching art type: {profile.art_type}")
            
            # Check interests overlap
            current_interests = set(i.lower() for i in current_profile.get_interests_list())
            user_interests = set(i.lower() for i in profile.get_interests_list())
            common_interests = current_interests & user_interests
            
            if common_interests:
                match_score += len(common_interests) * 20
                match_reasons.append(f"Common interests: {', '.join(common_interests)}")
            
            # Only include users with some match
            if match_score > 0:
                potential_matches.append({
                    'user': user,
                    'profile': profile,
                    'match_score': match_score,
                    'match_reasons': match_reasons,
                    'artworks_count': Artwork.objects.filter(user=user).count(),
                })
    
    # Sort by match score
    potential_matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render(request, 'pallate/find_collaborators.html', {
        'matches': potential_matches,
        'current_profile': current_profile,
    })


@login_required
def collaboration_feedback(request, collaboration_id):
    """Submit feedback/rating for a collaboration"""
    collaboration = get_object_or_404(Collaboration, id=collaboration_id)
    
    # Check if user already submitted feedback
    existing_feedback = CollaborationFeedback.objects.filter(
        collaboration=collaboration,
        reviewer=request.user
    ).first()
    
    if request.method == 'POST':
        if existing_feedback:
            form = CollaborationFeedbackForm(request.POST, instance=existing_feedback)
        else:
            form = CollaborationFeedbackForm(request.POST)
        
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.collaboration = collaboration
            feedback.reviewer = request.user
            feedback.save()
            
            # Notify collaboration owner
            if request.user != collaboration.user:
                Notification.objects.create(
                    user=collaboration.user,
                    text=f"{request.user.username} rated your collaboration '{collaboration.title}' - {feedback.rating}/5"
                )
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('pallate:collaboration_detail', pk=collaboration_id)
    else:
        if existing_feedback:
            form = CollaborationFeedbackForm(instance=existing_feedback)
        else:
            form = CollaborationFeedbackForm()
    
    # Get all feedbacks for this collaboration
    all_feedbacks = CollaborationFeedback.objects.filter(
        collaboration=collaboration
    ).select_related('reviewer').order_by('-created_at')
    
    # Calculate average rating
    if all_feedbacks.exists():
        avg_rating = sum(f.rating for f in all_feedbacks) / len(all_feedbacks)
    else:
        avg_rating = 0
    
    return render(request, 'pallate/collaboration_feedback.html', {
        'collaboration': collaboration,
        'form': form,
        'existing_feedback': existing_feedback,
        'all_feedbacks': all_feedbacks,
        'avg_rating': round(avg_rating, 1),
    })


@login_required
def featured_artists(request):
    """Display featured artists"""
    featured_profiles = Profile.objects.filter(
        is_featured=True
    ).select_related('user').order_by('-user__date_joined')
    
    # Get their artworks
    featured_data = []
    for profile in featured_profiles:
        artworks = Artwork.objects.filter(user=profile.user).order_by('-created_at')[:3]
        featured_data.append({
            'profile': profile,
            'user': profile.user,
            'artworks': artworks,
            'total_artworks': Artwork.objects.filter(user=profile.user).count(),
        })
    
    return render(request, 'pallate/featured_artists.html', {
        'featured_data': featured_data,
    })


@login_required
def collaboration_matches(request, collaboration_id):
    """View suggested matches for a specific collaboration"""
    collaboration = get_object_or_404(Collaboration, id=collaboration_id)
    
    # Only owner can see matches
    if collaboration.user != request.user:
        messages.error(request, "You don't have permission to view these matches.")
        return redirect('pallate:collaboration_detail', pk=collaboration_id)
    
    # Generate matches if not exists
    existing_matches = CollaborationMatch.objects.filter(collaboration=collaboration)
    
    if not existing_matches.exists():
        # Generate matches based on collaboration owner's profile
        owner_profile = collaboration.owner.profile
        potential_users = User.objects.exclude(id=request.user.id).select_related('profile')
        
        for user in potential_users:
            if hasattr(user, 'profile'):
                profile = user.profile
                match_score = 0
                
                # Art type match
                if owner_profile.art_type and profile.art_type:
                    if owner_profile.art_type.lower() in profile.art_type.lower() or \
                       profile.art_type.lower() in owner_profile.art_type.lower():
                        match_score += 50
                
                # Interests overlap
                owner_interests = set(i.lower() for i in owner_profile.get_interests_list())
                user_interests = set(i.lower() for i in profile.get_interests_list())
                common_interests = owner_interests & user_interests
                
                if common_interests:
                    match_score += len(common_interests) * 20
                
                # Create match if score > 0
                if match_score > 0:
                    CollaborationMatch.objects.create(
                        collaboration=collaboration,
                        suggested_user=user,
                        match_score=match_score
                    )
    
    # Get all matches
    matches = CollaborationMatch.objects.filter(
        collaboration=collaboration
    ).select_related('suggested_user__profile').order_by('-match_score')
    
    return render(request, 'pallate/collaboration_matches.html', {
        'collaboration': collaboration,
        'matches': matches,
    })


# ============================================
# PASSWORD RESET (No Email Required)
# ============================================

def password_reset_no_email(request):
    """Step 1: Enter username/email to find account"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            
            # Try to find user by username or email
            try:
                if '@' in username_or_email:
                    user = User.objects.get(email=username_or_email)
                else:
                    user = User.objects.get(username=username_or_email)
                
                # Check if user has security question set
                if hasattr(user, 'profile') and user.profile.security_question:
                    # Store user_id in session for next step
                    request.session['reset_user_id'] = user.id
                    return redirect('pallate:password_reset_security_question')
                else:
                    messages.error(request, 'No security question set for this account. Please contact an administrator.')
                    return redirect('pallate:login')
                    
            except User.DoesNotExist:
                messages.error(request, 'No account found with that username or email.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'pallate/password_reset_no_email.html', {'form': form})


def password_reset_security_question(request):
    """Step 2: Answer security question"""
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('pallate:password_reset_no_email')
    
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
    except (User.DoesNotExist, Profile.DoesNotExist):
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('pallate:password_reset_no_email')
    
    if request.method == 'POST':
        form = SecurityQuestionAnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['security_answer'].strip().lower()
            stored_answer = profile.security_answer.strip().lower()
            
            if answer == stored_answer:
                # Correct answer, proceed to password reset
                return redirect('pallate:password_reset_new_password')
            else:
                messages.error(request, 'Incorrect answer. Please try again.')
    else:
        form = SecurityQuestionAnswerForm()
    
    return render(request, 'pallate/password_reset_security_question.html', {
        'form': form,
        'security_question': profile.security_question,
        'username': user.username
    })


def password_reset_new_password(request):
    """Step 3: Set new password"""
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('pallate:password_reset_no_email')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('pallate:password_reset_no_email')
    
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            
            # Clear session
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            
            messages.success(request, 'Password reset successful! You can now log in with your new password.')
            return redirect('pallate:login')
    else:
        form = NewPasswordForm()
    
    return render(request, 'pallate/password_reset_new_password.html', {
        'form': form,
        'username': user.username
    })