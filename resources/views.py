from django.shortcuts import render, redirect
from .models import File, Link, Resource
from transformations.models import Transformation
from topics.models import Topic
from .forms import LinkForm, FileForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from transformations.views import MyDeleteMixin
from .helpers import viewthisresource, resourceformfactory
from .forms import ResourceFilterForm


# FILE MGMT VIEWS AND FORMS

def ResourceList(request):
     
     form = ResourceFilterForm()
     resource_list = Resource.objects.all()
     
     assert False, resource_list
     
     if request.GET:
          
          # So much filtering!
          if request.GET['type'] != '': resource_list.filter(type=request.GET['type'])
          if request.GET['category'] != '': resource_list.filter(category=request.GET['category'])
          if request.GET['topic'] != '': resource_list.filter(Topic.objects.get(pk=request.GET['topic']).resourceTreeQuery())
          if request.GET['transformation'] != '': resource_list.filter(transformation=request.GET['transformation'])
          if request.GET['ministry'] != '': resource_list.filter(transformation__ministry__abbrev=request.GET['ministry'])
          
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
     model = File
     form_class = FileForm
     template_name='resources/resource_form.html'
     success_message = 'File updated.'
     
class ViewLink(generic.DetailView):
     model = Link
     template_name = 'resources/resource_detail.html'
     
class ViewFile(generic.DetailView):
     model = File
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
     
     model = File
     # success_url = reverse_lazy('index')
     template_name = 'core/confirm_delete.html'
     
# SECOND TRY

def AddResource(request, type, base=None, slug=None):
     
     if request.method == 'POST':
          
          resource_form = resourceformfactory(type, base, request.POST, request.FILES, False)
          
          if resource_form.is_valid():
               new_resource = resource_form.save(commit=False)
               new_resource.type = type
               new_resource.created_by = request.user
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
               
     return render(request, 'resources/resource_form.html', {'form':resource_form, 'type':type,} )