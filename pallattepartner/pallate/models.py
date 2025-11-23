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

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
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