from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from autoslug import AutoSlugField
from django.urls import reverse 
from functools import reduce
import operator

class Topic(MPTTModel):
    title = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subtopics', db_index=True)
    description = models.CharField(max_length=240,blank=True)
    slug = AutoSlugField(populate_from='title')
    
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def __str__(self):
        return self.title
        
    def resources(self):
        return self.resource_set.all()
        
    def resourcefamily(self):
        
        from resources.models import Resource
        
        tree = self.get_descendants(include_self=True)
        q_list = [Resource.objects.filter(topics=leaf) for leaf in tree ]
        
        # Turns list of querysets into a bunch of queries connected by 'OR'
        combined_q = q_list.pop()
        for q in q_list:
            combined_q |= q
            
        return combined_q.distinct()

    def get_absolute_url(self):
        return reverse('topic-detail', args=[str(self.slug)])
        
        
    
