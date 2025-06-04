from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Create missing profiles for users'

    def handle(self, *args, **options):
        users_without_profiles = []

        for user in User.objects.all():
            try:
                profile = user.profile
                self.stdout.write(f"✅ {user.username} has profile")
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)
                users_without_profiles.append(user.username)
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created profile for {user.username}")
                )

        if not users_without_profiles:
            self.stdout.write(
                self.style.SUCCESS("All users already have profiles!")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created profiles for {len(users_without_profiles)} users: {', '.join(users_without_profiles)}"
                )
            )

