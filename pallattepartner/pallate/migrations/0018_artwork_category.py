# Generated migration for adding category field to Artwork model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pallate', '0017_profile_availability_status_profile_hourly_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='category',
            field=models.CharField(
                choices=[
                    ('digital', 'Digital Art'),
                    ('traditional', 'Traditional Art'),
                    ('illustration', 'Illustration'),
                    ('concept', 'Concept Art'),
                    ('character', 'Character Design'),
                    ('landscape', 'Landscape'),
                    ('portrait', 'Portrait'),
                    ('abstract', 'Abstract'),
                    ('fantasy', 'Fantasy'),
                    ('scifi', 'Sci-Fi'),
                    ('anime', 'Anime/Manga'),
                    ('photography', 'Photography'),
                    ('3d', '3D Art'),
                    ('pixel', 'Pixel Art'),
                    ('other', 'Other')
                ],
                default='other',
                help_text='Select artwork category',
                max_length=50
            ),
        ),
    ]
