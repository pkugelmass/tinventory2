from django.contrib import admin
from .models import Topic

admin.site.register(Topic)

class TopicsAdmin(admin.ModelAdmin):
    topics = ('title','parent','description')