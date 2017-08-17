from django.db import models
from django.core.urlresolvers import reverse
from transformations.models import Transformation
from topics.models import Topic
from mptt.models import TreeManyToManyField
from django.contrib.admin.widgets import FilteredSelectMultiple
import os


class Resource_Tag(models.Model):
     name = models.CharField(max_length=20)
     
     class Meta:
          ordering = ['name']
          
     def __str__(self):
          return self.name

class Resource(models.Model):
     
     CATEGORIES = (
          ('example', 'Templates, Tools and Examples'),
          ('reading', 'Guides, Articles, Books and other Reference'),
          ('lessons', 'Lessons Learned from Real Experience'),
     )

     transformation = models.ForeignKey('transformations.Transformation', blank=True)
     title = models.CharField('Title', max_length=50)
     description = models.TextField(help_text='Describe the resource and how it may be useful to others.')
     topics = TreeManyToManyField('topics.Topic', blank=True, help_text="Ctrl-click to choose all that apply.")
     category = models.CharField('Resource Category',max_length=10,choices=CATEGORIES)
     date_modified = models.DateTimeField(auto_now=True)
     
     class Meta:
           abstract = True
     
     def __str__(self):
          return self.title
          
     def tag_list(self):
          return ', '.join(map(str, self.tags.all()))
          
class Attachment(Resource):

     def get_upload_path(instance, filename):
          return os.path.join('transformations', str(instance.transformation.slug), filename)
     
     resource = models.FileField("Attachment",upload_to=get_upload_path)
     
     def get_absolute_url(self):
        return reverse('view-file', kwargs={'pk': self.pk})
        
     @property
     def filename(self):
          return os.path.basename(self.resource.name)
        
     @property
     def type(self):
          return 'File'
          
     # NB Deleting doesn't actually delete the file.

class Link(Resource):
     resource = models.URLField("Link")
     
     def get_absolute_url(self):
        return reverse('view-link', kwargs={'pk': self.pk})
        
     @property
     def type(self):
          return 'Link'
          
