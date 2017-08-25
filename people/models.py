from django.db import models
from django.contrib.auth.models import User
from transformations.models import Ministry
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
import os

class Profile(models.Model):

    def get_upload_path(instance, filename):
        return os.path.join('users', datetime.now().strftime("%y-%m-%d"), filename)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ministry = models.ForeignKey('transformations.Ministry', blank=True)
    role = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to=get_upload_path, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True, default=datetime.now)
    
    def get_absolute_url(self):
        return "/users/%s" % (self.user.username)
        
    def __str__(self):
        return "Profile for %s" % (self.user.get_full_name())
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()