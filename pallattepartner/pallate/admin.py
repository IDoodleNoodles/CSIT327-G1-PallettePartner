from django.contrib import admin
from .models import Palette, Profile, Collaboration, Message, Notification, Artwork, Favorite

# Register your models here.
admin.site.register(Palette)
admin.site.register(Profile)
admin.site.register(Collaboration)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Artwork)
admin.site.register(Favorite)
