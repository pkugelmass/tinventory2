from django.contrib import admin
from .models import Transformation, Ministry, Transformation_Tag

class TransformationAdmin(admin.ModelAdmin):
    list_display=['title', 'ministries_list', 'category', 'status', 'date_modified', 'archived']
    list_editable=['archived', 'status', 'category']
    

admin.site.register(Transformation, TransformationAdmin)
admin.site.register(Ministry)
admin.site.register(Transformation_Tag)
