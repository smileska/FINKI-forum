from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
        (5, 'Fourth Year+'),
        (6, 'Graduate'),
        (7, 'Masters'),
    ]

    FACULTY_CHOICES = [
        ('KN', 'Computer Science'),
        ('SIIS', 'Software Engineering And Information Systems'),
        ('IMB', 'Internet, Networks and Security'),
        ('KI', 'Computer Engineering'),
        ('PIT', 'Appliance of Information Technology'),
        ('KE', 'Computer Education'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, default='KN')
    student_id = models.CharField(max_length=20, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            print(f"Error creating profile for {instance.username}: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)
    except Exception as e:
        print(f"Error saving profile for {instance.username}: {e}")