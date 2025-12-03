from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pallattepartner.pallate.models import (
    Palette, Profile, Collaboration, CollaborationRole, 
    CollaborationApplication, CollaborationFile, CollaborationTask,
    Message, Notification, Artwork, ArtworkComment, Favorite,
    CollaborationFeedback, CollaborationMatch
)


class Command(BaseCommand):
    help = 'Clear all data from database tables except users, keeping the schema intact'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting data deletion (keeping all users)...'))
        
        # Delete in order to respect foreign key constraints
        models_to_clear = [
            ('CollaborationMatch', CollaborationMatch),
            ('CollaborationFeedback', CollaborationFeedback),
            ('Favorite', Favorite),
            ('ArtworkComment', ArtworkComment),
            ('Artwork', Artwork),
            ('Notification', Notification),
            ('Message', Message),
            ('CollaborationTask', CollaborationTask),
            ('CollaborationFile', CollaborationFile),
            ('CollaborationApplication', CollaborationApplication),
            ('CollaborationRole', CollaborationRole),
            ('Collaboration', Collaboration),
            ('Profile', Profile),
            ('Palette', Palette),
        ]
        
        total_deleted = 0
        
        for model_name, model in models_to_clear:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Deleted {count} {model_name} records')
                )
                total_deleted += count
            else:
                self.stdout.write(f'  {model_name}: No records to delete')
        
        # Show user count
        user_count = User.objects.count()
        self.stdout.write(
            self.style.WARNING(f'  Kept all {user_count} User record(s)')
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Data clearing complete! Total records deleted: {total_deleted}')
        )
        self.stdout.write(
            self.style.WARNING('Note: All users preserved. Database tables and schema remain intact.')
        )
