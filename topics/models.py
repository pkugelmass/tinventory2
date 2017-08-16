from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from autoslug import AutoSlugField


class Topic(MPTTModel):
    title = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subtopics', db_index=True)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='title')
    
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def __str__(self):
        return self.title
        
    def resources(self):
          related_resources = list(self.attachment_set.all()) + list(self.link_set.all())
          return sorted(related_resources, key=lambda r: r.date_modified, reverse=True)
          
    
