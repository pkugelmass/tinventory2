from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_view=['user', 'ministry', 'role', 'profile_picture', 'date_created', 'last_visit']
admin.site.register(Profile, ProfileAdmin)