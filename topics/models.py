from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from autoslug import AutoSlugField
from django.urls import reverse 


class Topic(MPTTModel):
    title = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subtopics', db_index=True)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='title')
    
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def __str__(self):
        return self.title
        
    # For pulling out the resources lists -- THIS IS BAD PROGRAMMING SORRY
        
    def resources(self):
          related_resources = list(self.attachment_set.all()) + list(self.link_set.all())
          return sorted(related_resources, key=lambda r: r.date_modified, reverse=True)
          
    def examples(self):
        related_resources = list(self.attachment_set.filter(category='examples')) + \
            list(self.link_set.filter(category="examples"))
        return sorted(related_resources, key=lambda r: r.date_modified, reverse=True)
        
    def readings(self):
        related_resources = list(self.attachment_set.filter(category='reading')) + \
            list(self.link_set.filter(category="reading"))
        return sorted(related_resources, key=lambda r: r.date_modified, reverse=True)
        
    def lessons(self):
        related_resources = list(self.attachment_set.filter(category='lessons')) + \
            list(self.link_set.filter(category="lessons"))
        return sorted(related_resources, key=lambda r: r.date_modified, reverse=True)
            
        
    # def readings(self):
    #     return [ r for r in list(self.resources) if r.category=="reading" ]
        
    # def lessons(self):
    #     return [ r for r in list(self.resources) if r.category=="lessons" ]
        
    def get_absolute_url(self):
        return reverse('topic-detail', args=[str(self.slug)])
        
        
    
