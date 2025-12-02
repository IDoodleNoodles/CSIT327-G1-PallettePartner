from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Palette(models.Model):
	"""A minimal model representing a color palette shared by an artist."""
	name = models.CharField(max_length=100)
	colors = models.CharField(max_length=255, help_text='Comma-separated hex colors')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} ({self.colors})"
	

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    art_type = models.CharField(max_length=100, blank=True, default='')
    portfolio = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    interests = models.TextField(blank=True, default='', help_text='Comma-separated interests (e.g., Fantasy Art, Portraits, Digital Painting)')
    is_featured = models.BooleanField(default=False, help_text='Featured artist status')
    
    # Security Question for Password Reset (no email needed)
    security_question = models.CharField(max_length=255, blank=True, default='', help_text='Security question for password recovery')
    security_answer = models.CharField(max_length=255, blank=True, default='', help_text='Answer to security question (stored hashed)')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_interests_list(self):
        """Returns list of interests from comma-separated string"""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',') if interest.strip()]
        return []
    
    def matches_criteria(self, other_profile):
        """Check if this profile matches with another based on art_type and interests"""
        if not other_profile:
            return False
        
        # Check art_type match
        art_type_match = self.art_type and other_profile.art_type and \
                        self.art_type.lower() in other_profile.art_type.lower() or \
                        other_profile.art_type.lower() in self.art_type.lower()
        
        # Check interests overlap
        self_interests = set(i.lower() for i in self.get_interests_list())
        other_interests = set(i.lower() for i in other_profile.get_interests_list())
        interests_match = bool(self_interests & other_interests)
        
        return art_type_match or interests_match
    
class Collaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Message(models.Model):
    collaboration = models.ForeignKey(
        Collaboration,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    reaction = models.CharField(max_length=10, blank=True)  # e.g. "❤️", "👍"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        base = f"{self.sender.username}: "
        if self.text:
            return base + self.text[:30]
        if self.image:
            return base + "[image]"
        return base + "[empty]"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.text}"


class Artwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='artworks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class ArtworkComment(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.artwork.title}: {self.text[:30]}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'artwork')

    def __str__(self):
        return f"{self.user.username} favorited {self.artwork.title}"


class CollaborationFeedback(models.Model):
    """Feedback and rating system for completed collaborations"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    collaboration = models.ForeignKey(Collaboration, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedbacks')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('collaboration', 'reviewer')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.username} rated '{self.collaboration.title}' - {self.rating}/5"


class CollaborationMatch(models.Model):
    """Suggested matches for collaborations based on art type and interests"""
    collaboration = models.ForeignKey(Collaboration, on_delete=models.CASCADE, related_name='suggested_matches')
    suggested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaboration_suggestions')
    match_score = models.IntegerField(default=0, help_text='Higher score = better match')
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    is_contacted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('collaboration', 'suggested_user')
        ordering = ['-match_score', '-created_at']
    
    def __str__(self):
        return f"Match: {self.suggested_user.username} for '{self.collaboration.title}' (score: {self.match_score})"