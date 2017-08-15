from django.contrib import admin
from .models import Topic
from django_mptt_admin.admin import DjangoMpttAdmin



class TopicAdmin(DjangoMpttAdmin):
    pass
    
admin.site.register(Topic, TopicAdmin)