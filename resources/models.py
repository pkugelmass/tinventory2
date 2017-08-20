from django.db import models
from django.core.urlresolvers import reverse
from transformations.models import Transformation
from topics.models import Topic
from django.contrib.auth.models import User
from mptt.models import TreeManyToManyField
from django.conf import settings
from autoslug import AutoSlugField
import datetime
import os

class Resource(models.Model):
     
     CATEGORIES = (
          ('example', 'Real World Example'),
          ('template', 'Tool or Template'),
          ('reading', 'Theory, Guide, Article or Book'),
          ('lessons', 'Lessons Learned'),
     )
     
     RESOURCE_TYPES = (
          ('file', 'File'),
          ('link', 'Link')
     )
     
     # def resourceTypeList(self):
     #      return [ ( x , x.__name__.capitalize() ) for x in self.__class__.__subclasses__()]
     
     def get_upload_path(instance, filename):
          return os.path.join('resources', datetime.date.today().strftime("%y-%m-%d"), filename)
          
     def filename(self):
        return os.path.basename(self.file.name)

     type = models.CharField('Resource Type', max_length=5, choices=RESOURCE_TYPES)
     
     title = models.CharField('Title', max_length=50)
     description = models.TextField(help_text='Describe the resource and how it may be useful to others.')
     slug = AutoSlugField(populate_from='title', unique=True)
     
     file = models.FileField("File",upload_to=get_upload_path, blank=True, null=True)
     link = models.URLField("Link", help_text="The URL (address), starting with \'http.\'", blank=True, null=True)
     
     category = models.CharField('Resource Category',max_length=10,choices=CATEGORIES)
     transformation = models.ForeignKey('transformations.Transformation', blank=True, null=True)
     topics = TreeManyToManyField('topics.Topic', help_text="Ctrl-click to choose all that apply.", blank=True)
     
     created_by = models.ForeignKey('auth.User')
     date_modified = models.DateTimeField(auto_now=True)
     
     def __init__(self, *args, **kwargs):
          
          super(Resource, self).__init__(*args, **kwargs)

          if not self.__class__.__subclasses__():
               self.type = self.__class__.__name__.lower() # If there are no subclasses, call it a resource object.
               
          else:
               
               subclass = [x for x in self.__class__.__subclasses__() if x.__name__.lower() == self.type]
               
               if subclass:
                    self.__class__ = subclass[0]
               else:
                    raise TypeError("Please specify a type for this resource.") # But if there are subclasses, 'resource' won't do.
     
     def __str__(self):
          return self.title
          
     def get_absolute_url(self):
          return reverse('view-resource', kwargs={'slug': self.slug})
          
     class Meta:
          ordering = ['-date_modified']
          
class ProxyManager(models.Manager):
     def get_query_set(self):
          return super(ProxyManager, self).get_query_set().filter(type=self.model.__name__.lower())

class File(Resource):
     
     objects = ProxyManager()
     
     class Meta:
          proxy = True

class Link(Resource):
     
     objects = ProxyManager()
     
     class Meta:
          proxy = True
          
