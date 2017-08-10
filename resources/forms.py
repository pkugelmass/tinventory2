from django import forms
from .models import Attachment, Link
from transformations.models import Transformation

class AttachmentForm(forms.ModelForm):
     class Meta:
          model = Attachment
          fields = ['resource','title','description','transformation', 'tags']
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}
          
class LinkForm(forms.ModelForm):
     class Meta:
          model = Link
          fields = ['resource','title','description','transformation', 'tags'] 
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}