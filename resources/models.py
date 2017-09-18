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
from people.models import Action
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum


class Resource(models.Model):
     
     CATEGORIES = (
          ('example', 'Real World Example'),
          ('template', 'Tool or Template'),
          ('reading', 'Theory, Guide, Article or Book'),
          ('lessons', 'Lessons Learned'),
     )
     
     RESOURCE_TYPES = (
          ('file', 'File'),
          ('link', 'Link'),
          ('post', 'Post'),
     )
     
     # def resourceTypeList(self):
     #      return [ ( x , x.__name__.capitalize() ) for x in self.__class__.__subclasses__()]
     
     def get_upload_path(instance, filename):
          return os.path.join('resources', datetime.date.today().strftime("%y-%m-%d"), filename)
          
     def filename(self):
        return os.path.basename(self.file.name)

     type = models.CharField('Resource Type', max_length=5, choices=RESOURCE_TYPES)
     
     title = models.CharField('Title', max_length=80)
     description = models.CharField(max_length=255, help_text='Describe the resource and how it may be useful to others.')
     slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
     
     file = models.FileField("File",upload_to=get_upload_path, blank=True, null=True)
     link = models.URLField("Link", help_text="The URL (address), starting with \'http.\'", blank=True, null=True)
     post = RichTextUploadingField("Post", help_text="Type your post here.",  blank=True, null=True)
     
     category = models.CharField('Resource Category',max_length=10,choices=CATEGORIES)
     transformation = models.ForeignKey('transformations.Transformation', blank=True, null=True)
     topics = TreeManyToManyField('topics.Topic', help_text="Ctrl-click to choose all that apply.", blank=True)
     
     credit = models.CharField('Credit',max_length=100,help_text='Who made or contributed to this?', blank=True, null=True)
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
          
     class Meta:
          ordering = ['-date_modified']
          
     def actions(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Resource))
          
     def created(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Resource), verb="added").first()
          
     def modified(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Resource), verb="updated").first()
          
     def total_stars(self):
          stars = Review.objects.filter(resource=self).aggregate(total=Sum('rating'))
          return stars['total']
          
          
     def related_objects(self):
          bases = [ x for x in self.topics.all()]
          # if self.transformation: 
          #      bases += self.transformation
          return bases
          
class ProxyManager(models.Manager):
     def get_query_set(self):
          return super(ProxyManager, self).get_query_set().filter(type=self.model.__name__.lower())

class File(Resource):
     
     objects = ProxyManager()
     
     class Meta:
          proxy = True
          
     def get_absolute_url(self):
          return reverse('view-file', kwargs={'slug': self.slug})

class Link(Resource):
     
     objects = ProxyManager()
     
     class Meta:
          proxy = True
          
     def get_absolute_url(self):
          return reverse('view-link', kwargs={'slug': self.slug})
          
class Post(Resource):
     
     objects = ProxyManager()
     
     class Meta:
          proxy = True
          
     def get_absolute_url(self):
          return reverse('view-post', kwargs={'slug': self.slug})
          
class Review(models.Model):
     
     REVIEW_DESCRIPTIONS = (
          (2,'Really Great'),
          (1,'Great'),
          (0,'Interesting'),
          )
     
     rating = models.SmallIntegerField(
          'Your Rating', 
          default=0, 
          choices=REVIEW_DESCRIPTIONS, 
          validators=[MaxValueValidator(2),MinValueValidator(0)])
     
     user = models.ForeignKey(settings.AUTH_USER_MODEL)
     resource = models.ForeignKey(Resource, related_name='reviews')
     
     review = models.TextField(blank=True,null=True, help_text='What\'s valuable about this resource?')
     date_modified = models.DateTimeField(auto_now=True)
     
     class Meta:
          unique_together = ("user", "resource")
          ordering = ['-date_modified']
     
     def description(self):
          return self.REVIEW_DESCRIPTIONS[2-self.rating][1]
          
     def __str__(self):
          stars = '*' * self.rating
          return '%s Review of %s by %s' % (stars, self.resource, self.user)
     