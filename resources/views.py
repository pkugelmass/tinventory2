from django.shortcuts import render, redirect
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
from .helpers import viewthisresource, resourceformfactory
from .forms import ResourceFilterForm
from django.db.models import Q


# FILE MGMT VIEWS AND FORMS

def ResourceList(request):
     
     form = ResourceFilterForm()
     resource_list = list(Link.objects.all()) + list(Attachment.objects.all())
     resource_list = sorted(resource_list, key=lambda r: r.date_modified, reverse=True)
     
     if request.GET:
          
          # Get ready for some bad programming!
          
          q_list = []
          if request.GET['category'] != '': q_list = q_list + [Q(category=request.GET['category'])]
          #if request.GET['topic'] != '': q_list = q_list + [Q(topics=request.GET['topic'])]
          if request.GET['transformation'] != '': q_list = q_list + [Q(transformation=request.GET['transformation'])]
          if request.GET['ministry'] != '': q_list = q_list + [Q(transformation__ministry__abbrev=request.GET['ministry'])]
          
          
          if len(q_list) > 0:
               combined_q = q_list.pop()
               for q in q_list:
                    combined_q &= q
          else:
               combined_q = Q(pk__gt=0)
          
          # Filter the query based on those arguments (if any).
          links = Link.objects.filter(combined_q)
          attachments = Attachment.objects.filter(combined_q)
          
          # Zero/"filter" out the 'other' resource type if one has been set.
          if request.GET['resourcetype'] == 'File': links = []
          if request.GET['resourcetype'] == 'Link': attachments = []
          
          
          # Combine it into a resource list:
          resource_list = list(links) + list(attachments)
          resource_list = sorted(resource_list, key=lambda r: r.date_modified, reverse=True)
          
          # Now filter for the topic's whole family...
          if request.GET['topic'] != '': 
               topiczz = Topic.objects.get(pk=request.GET['topic'])
               topic_resources = topiczz.resourcefamily()
               topic_resources_set = set(topic_resources)
               resource_set = set(resource_list)
               resource_list = list(set.intersection(topic_resources_set,resource_set))
          
          # Set the forms to show the criteria used when they are reloaded.
          for fieldname in request.GET:
               form.fields[fieldname].initial = request.GET[fieldname]
     
     context = {
          'resources':resource_list,
          'r_filter_form':form,
     }
     
     return render(request, 'resources/resource_list.html', context)
     
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

def AddResource(request, type, base=None, slug=None):
     
     if request.method == 'POST':
          
          resource_form = resourceformfactory(type, base, request.POST, request.FILES, False)
          
          if resource_form.is_valid():
               new_resource = resource_form.save()
               new_resource.save()
               messages.success(request,'Your %s \'%s\' has been saved.' % (type, new_resource.title))
               
               return viewthisresource(new_resource) #helper function that redirects to resource detail regardless of type...

     else:
          
          initial_data = {}
          
          if base == 'topic' and slug != None: 
                    
                    initial_data = {'topics':[Topic.objects.get(slug=slug)]}
          elif base == 'transformation' and slug != None: 
                    initial_data = {'transformation':Transformation.objects.get(slug=slug)}
               
          resource_form = resourceformfactory(type, base, initial_data, None, True)
               
     return render(request, 'resources/resource_form.html', {'form':resource_form} )