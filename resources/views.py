from django.shortcuts import render
from .models import Attachment, Link
from transformations.models import Transformation
from topics.models import Topic
from .forms import LinkForm, AttachmentForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from transformations.views import MyDeleteMixin


# FILE MGMT VIEWS AND FORMS

def ResourceList(request):
     
     resource_list = list(Link.objects.all()) + list(Attachment.objects.all())
     resource_list = sorted(resource_list, key=lambda r: r.date_modified, reverse=True)
     
     return render(request, 'resources/resource_list.html', {'resources':resource_list})

class ResourceFormMixin:
     template_name='resources/resource_form.html'
     
     def get_initial(self):
          initial = super(generic.edit.CreateView, self).get_initial()
          try:
               initial['transformation'] = Transformation.objects.get(pk=self.kwargs['tID'])
          except:
               pass
          return initial
          
class AddLink(SuccessMessageMixin, ResourceFormMixin, generic.edit.CreateView):
     model = Link
     form_class = LinkForm
     success_message = 'New link added.'
     
class AddFile(SuccessMessageMixin, ResourceFormMixin, generic.edit.CreateView):
     model = Attachment
     form_class = AttachmentForm
     success_message = 'New file added.'
     
class EditLink(SuccessMessageMixin,generic.edit.UpdateView):
     model = Link
     form_class = LinkForm
     template_name='resources/resource_form.html'
     success_message = 'Link updated.'
     
class EditFile(SuccessMessageMixin,generic.edit.UpdateView):
     model = Attachment
     form_class = AttachmentForm
     template_name='resources/resource_form.html'
     success_message = 'File updated.'
     
class ViewLink(generic.DetailView):
     model = Link
     template_name = 'resources/resource_detail.html'
     
class ViewFile(generic.DetailView):
     model = Attachment
     template_name = 'resources/resource_detail.html'

class DeleteLink(MyDeleteMixin, generic.edit.DeleteView):

     def get_success_url(self):
          # Assuming there is a ForeignKey from Comment to Post in your model
          transformation = self.object.transformation
          return reverse_lazy( 'transformation-detail', kwargs={'pk': transformation.pk})

     model = Link
     success_url = reverse_lazy('index')
     template_name = 'core/confirm_delete.html'
     
     
class DeleteFile(MyDeleteMixin, generic.edit.DeleteView):
     
     def get_success_url(self):
          # Assuming there is a ForeignKey from Comment to Post in your model
          transformation = self.object.transformation
          return reverse_lazy( 'transformation-detail', kwargs={'pk': transformation.pk})
     
     model = Attachment
     # success_url = reverse_lazy('index')
     template_name = 'core/confirm_delete.html'
     
# SECOND TRY

def AddResource(request, type, topic_slug=None, trans_slug=None):

    data = {}
    if topic_slug: data = {'topics':[Topic.objects.get(slug=topic_slug)]}
    if trans_slug: data = {'transformation':Transformation.objects.get(slug=trans_slug)}

    if type == 'link':
        resource_form = LinkForm(initial=data)
    elif type == 'file':
        resource_form = AttachmentForm(initial=data)
    else:
        raise FieldError('Type of resource not identified.')
        
    return render(
        request,
        'resources/resource_form.html',
        {'form':resource_form}
        )