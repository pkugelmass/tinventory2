from django.db import models
#from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField
import os

class Transformation(models.Model):
     title = models.CharField("Transformation Title", max_length=100)
     ministry = models.ManyToManyField('Ministry')
     description = models.TextField("High-Level Description")
     problem = models.TextField("What problem is it trying to solve?", blank=True)
     specific_orgs = models.CharField("Which specific areas or other organizations are involved?", max_length=240, blank=True)
     primary_contact = models.CharField("Primary Contact", max_length=100, blank=True)
     
     CATEGORIES = (
          ('structure', 'Structure/Process'),
          ('strategy', 'Strategy/Policy'),
          ('service', 'Service Delivery'),
          ('people', 'People Development'),
          ('all', 'All of the Above'),
     )
     
     STATUSES = (
          ('direction', 'Defining Direction'),
          ('design', 'Design Stage'),
          ('implementation', 'Implementation'),
          ('sustainment', 'Sustainment'),
          ('complete', 'Past Transformation')
     )
     
     category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)
     status = models.CharField(max_length=20, choices=STATUSES, blank=True)
     #tags = TaggableManager(blank=True)
     #tags = models.CharField(max_length=20, blank=True)
     archived = models.BooleanField(default=False)
     slug = AutoSlugField(populate_from='title')
     
     def get_absolute_url(self):
          return reverse('transformation-detail', kwargs={'pk':self.pk})
          
     def __str__(self):
          return self.title
          
     def ministries_list(self):
          return ', '.join(map(str, self.ministry.all()))

class MinistryManager(models.Manager):
     def choices_list(self):
          return ( ( m , m.long() ) for m in self.get_queryset() )

class Ministry(models.Model):
     abbrev = models.CharField(max_length=6)
     name = models.CharField(max_length=100)
     
     class Meta:
          ordering = ['abbrev']
     
     def __str__(self):
          return self.abbrev 
          
     def long(self):
          return self.abbrev + ' - ' + self.name
          
     objects = MinistryManager()
     
# RESOURCE/FILE MODELS
          
class Resource(models.Model):

     transformation = models.ForeignKey('transformation')
     title = models.CharField('Title', max_length=50, help_text="Give this resource a descriptive name.")
     description = models.TextField()
     #tags = TaggableManager(blank=True)
     tags = models.CharField(max_length=20, blank=True)
     date_modified = models.DateTimeField(auto_now=True)
     
     class Meta:
          abstract = True
     
     def __str__(self):
          return self.title
        
          
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