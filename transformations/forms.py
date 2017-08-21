from django import forms
from .models import Ministry, Transformation, Transformation_Tag

# FORM HELPER STUFF ---------

# Custom field class to add an empty choice at the top of the drop-down box.
class ChoiceFieldEmpty(forms.ChoiceField):
     
     def __init__(self,*args,**kwargs):
          super(ChoiceFieldEmpty,self).__init__(*args,**kwargs)
          self.choices = [('',' ')] + self.choices
          
# TRANSFORMATION FORMS ------------

class TransformationFilterForm(forms.Form):
     
     TAG_LIST = ( (tag,tag) for tag in Transformation_Tag.objects.all() )
     
     ministry__abbrev = ChoiceFieldEmpty(choices = Ministry.objects.choices_list(), label="Ministry", required=False)
     category = ChoiceFieldEmpty(choices = Transformation.CATEGORIES, label="Category", required=False)
     status = ChoiceFieldEmpty(choices = Transformation.STATUSES, label="Status", required=False)
     tags__name = ChoiceFieldEmpty(choices = TAG_LIST, label="Tag", required=False)
     
class TransformationForm(forms.ModelForm):
     
     class Meta:
          model = Transformation
          fields = ['title','ministry','specific_orgs','description','problem','category', \
               'status','primary_contact', 'tags']
          widgets = {
               'description':forms.Textarea(attrs={'rows':4,'cols':40}),
               'problem':forms.Textarea(attrs={'rows':4,'cols':40}),}
          help_texts = {
               'ministry':'You can select more than one. Ctrl-click to select all that apply.',
               'tags':'What are some other areas of focus? You can select more than one. Ctrl-click to select all that apply.',
               'category':'What is the primary focus?'
               }

     def __init__(self, *args, **kwargs):
          super(TransformationForm, self).__init__(*args, **kwargs)
          self.fields['ministry'].widget.attrs['size']='7'
          self.fields['tags'].widget.attrs['size']='7'