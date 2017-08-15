from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from autoslug import AutoSlugField

class Topic(MPTTModel):
    title = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subtopics', db_index=True)
    description = models.TextField
    slug = AutoSlugField(populate_from='title')
    
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def __str__(self):
        return self.title
