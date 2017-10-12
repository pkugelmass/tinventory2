from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# PROFILE ------------

class Profile(models.Model):

    def get_upload_path(instance, filename):
        return os.path.join('users', datetime.now().strftime("%y-%m-%d"), filename)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ministry = models.ForeignKey('transformations.Ministry', blank=True, null=True, related_name='profiles')
    role = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True, default=timezone.now)
    
    def get_absolute_url(self):
        return "/users/%s" % (self.user.username)
        
    def __str__(self):
        return "Profile for %s" % (self.user.get_full_name())
    
# ACTIVITY STREAM -------------

class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', db_index=True)
    verb = models.CharField(max_length=255)
    target_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_type', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering=('-created',)
        
    def __str__(self):
        return '%s - %s %s %s \'%s\'.' % (self.created.strftime('%m%d%y-%H%M'), self.user.get_full_name(), self.verb, self.target_type, self.target)