from django.contrib import admin
from .models import Transformation, Ministry, Transformation_Tag, Resource_Tag

admin.site.register(Transformation)
admin.site.register(Ministry)
admin.site.register(Transformation_Tag)
admin.site.register(Resource_Tag)
