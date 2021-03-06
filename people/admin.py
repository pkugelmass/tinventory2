from django.contrib import admin
from .models import Profile, Action

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_view=['user', 'ministry', 'role', 'profile_picture', 'date_created', 'last_visit']
    
admin.site.register(Profile, ProfileAdmin)

class ActionAdmin(admin.ModelAdmin):
    list_display=('__str__','user', 'verb', 'target', 'target_type', 'created')
    list_filter=('created',)
    search_fields = ('verb','target')
    
admin.site.register(Action, ActionAdmin)
    