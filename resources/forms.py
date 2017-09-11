from django import forms
from .models import File, Link, Resource, Post
from transformations.models import Transformation, Ministry
from topics.models import Topic
from transformations.forms import ChoiceFieldEmpty
from mptt.forms import TreeNodeChoiceField
from django.core.exceptions import ValidationError


class ValidateResourceFormMixin:
     
     def clean(self):
          
          cleaned_data = super(ValidateResourceFormMixin,self).clean()
          
          if cleaned_data['topics'].count() == 0 and cleaned_data['transformation'] == None:
               raise ValidationError("Please specify topics and/or a transformation.")

class FileForm(ValidateResourceFormMixin, forms.ModelForm):
     class Meta:
          model = File
          fields = ['file','title','description', 'category', 'transformation', 'topics']
          widgets = {
               'description':forms.Textarea(attrs={'rows':3,'cols':40}),
          }
          
     def __init__(self, *args, **kwargs):
          super(FileForm, self).__init__(*args, **kwargs)
          self.fields['topics'].widget.attrs['size']='15'
          self.fields['file'].required = True
          
class LinkForm(ValidateResourceFormMixin, forms.ModelForm):
     class Meta:
          model = Link
          fields = ['link','title','description', 'category', 'transformation', 'topics']
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}
          
     def __init__(self, *args, **kwargs):
          super(LinkForm, self).__init__(*args, **kwargs)
          
          self.fields['topics'].widget.attrs['size']='15'
          self.fields['link'].initial="http://"
          self.fields['link'].required = True
          
class PostForm(ValidateResourceFormMixin, forms.ModelForm):
     class Meta:
          model = Post
          fields = ['title','description', 'post', 'category', 'transformation', 'topics']
          
     def __init__(self, *args, **kwargs):
          super(PostForm, self).__init__(*args, **kwargs)
          
          self.fields['topics'].widget.attrs['size']='15'
          self.fields['description'].help_text='What is your post about?'
          self.fields['category'].initial='lessons'

          
class ResourceFilterForm(forms.Form):
     
     RESOURCE_TYPES = ( ('file', 'File'), ('link','Link'), ('post','Post'), )
     
     resourcetype = ChoiceFieldEmpty(
          choices=RESOURCE_TYPES, 
          label = 'Type', 
          required=False)
     
     category = ChoiceFieldEmpty(
          choices=Resource.CATEGORIES, 
          label = 'Resource Category', 
          required=False)
     
     topic = TreeNodeChoiceField(
          Topic.objects.all(), 
          label='Topic', 
          empty_label='', 
          required=False)
     
     transformation = forms.ModelChoiceField(
          Transformation.objects.all().order_by('title'),
          label='Transformation', 
          empty_label='', 
          required=False)
     
     ministry = forms.ModelChoiceField(
          Ministry.objects.all(), 
          label="Ministry", 
          empty_label='',
          required=False)

