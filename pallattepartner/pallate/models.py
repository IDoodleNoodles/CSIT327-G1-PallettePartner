from django.db import models


class Palette(models.Model):
	"""A minimal model representing a color palette shared by an artist."""
	name = models.CharField(max_length=100)
	colors = models.CharField(max_length=255, help_text='Comma-separated hex colors')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} ({self.colors})"
