from django.contrib import admin
from .models import Link, Attachment, Resource_Tag

admin.site.register(Link)
admin.site.register(Attachment)
admin.site.register(Resource_Tag)