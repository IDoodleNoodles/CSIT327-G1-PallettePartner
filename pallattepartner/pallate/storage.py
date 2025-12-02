"""
Custom storage backends for Supabase Storage integration.

Supabase Storage is S3-compatible, so we use django-storages with boto3.
This file provides custom storage classes for different media types.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class SupabaseMediaStorage(S3Boto3Storage):
    """
    Storage backend for user-uploaded media files (avatars, artworks, chat images).
    Uses Supabase Storage bucket configured via environment variables.
    """
    location = 'media'
    bucket_name = settings.SUPABASE_STORAGE_BUCKET_NAME
    # Remove https:// as boto3 adds it automatically
    custom_domain = f"{settings.SUPABASE_URL.replace('https://', '').replace('http://', '')}/storage/v1/object/public/{settings.SUPABASE_STORAGE_BUCKET_NAME}"
    file_overwrite = False  # Don't overwrite files with same name
    default_acl = None  # Use bucket's default ACL


class SupabaseStaticStorage(S3Boto3Storage):
    """
    Storage backend for static files (CSS, JS, icons) - for production deployment.
    Uses Supabase Storage bucket for serving static assets.
    """
    location = 'static'
    bucket_name = settings.SUPABASE_STORAGE_BUCKET_NAME
    # Remove https:// as boto3 adds it automatically
    custom_domain = f"{settings.SUPABASE_URL.replace('https://', '').replace('http://', '')}/storage/v1/object/public/{settings.SUPABASE_STORAGE_BUCKET_NAME}"
    file_overwrite = True  # Overwrite static files on collectstatic
    default_acl = None
