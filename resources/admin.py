from django.contrib import admin
from .models import Resource, Review

class ResourceAdmin(admin.ModelAdmin):
    list_display=['title','type','category','created_by']
    list_filter=['category', ('topics',admin.RelatedOnlyFieldListFilter),'type']
    view_on_site=True
admin.site.register(Resource, ResourceAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display=['resource','user','date_modified']
admin.site.register(Review, ReviewAdmin)