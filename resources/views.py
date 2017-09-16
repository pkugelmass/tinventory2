from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import File, Link, Resource, Post, Review
from transformations.models import Transformation
from topics.models import Topic
from .forms import LinkForm, FileForm, PostForm, MyReviewForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from transformations.views import MyDeleteMixin
from .helpers import viewthisresource, resourceformfactory
from .forms import ResourceFilterForm
from django.db.models import Q 
from people.helpers import create_action
from people.viewmixins import UpdatedActionMixin, CreateActionMixin

# FILE MGMT VIEWS AND FORMS

def ResourceList(request):
     
     form = ResourceFilterForm()
     resource_list = Resource.objects.all()
     
     if request.GET:
          
          q_list = []
          
          if request.GET['resourcetype'] != '': q_list = q_list + [Q(type=request.GET['resourcetype'])]
          if request.GET['category'] != '': q_list = q_list + [Q(category=request.GET['category'])]
          if request.GET['topic'] != '': q_list = q_list + [Q(pk__in=Topic.objects.get(pk=request.GET['topic']).resourcefamily())]
          if request.GET['transformation'] != '': q_list = q_list + [Q(transformation=request.GET['transformation'])]
          if request.GET['ministry'] != '': q_list = q_list + [Q(transformation__ministry=request.GET['ministry'])]
          
          if len(q_list) > 0: # Only if there is something to filter...
               
               combined_q = Q(pk__gt=0) # Initialize a combined query.
               
               while len(q_list) > 0:
                    combined_q &= q_list.pop()
               resource_list = resource_list.filter(combined_q) # Filter resources by the combined query.
          
          # Set the forms to show the criteria used when they are reloaded.
          for fieldname in request.GET:
               form.fields[fieldname].initial = request.GET[fieldname]
     
     context = {
          'resources':resource_list,
          'r_filter_form':form,
     }
     
     return render(request, 'resources/resource_list.html', context)
     
def AddResource(request, type, base=None, slug=None):
     
     if request.method == 'POST':
          
          resource_form = resourceformfactory(type, base, request.POST, request.FILES, False)
          
          if resource_form.is_valid():
               new_resource = resource_form.save(commit=False)
               new_resource.type = type
               new_resource.created_by = request.user
               new_resource.save()
               resource_form.save_m2m() # Who knew that save_m2m must happon on the form, not the saved object...
               messages.success(request,'Your %s \'%s\' has been saved.' % (type, new_resource.title))
               
               create_action(request.user, 'added', new_resource)
               
               return viewthisresource(new_resource) #helper function that redirects to resource detail regardless of type...

     else:
          
          initial_data = {}
          
          if base == 'topic' and slug != None: 
               initial_data = {'topics':[Topic.objects.get(slug=slug)]}
          elif base == 'transformation' and slug != None: 
               initial_data = {'transformation':Transformation.objects.get(slug=slug)}
               
          resource_form = resourceformfactory(type, base, initial_data, None, True)
               
     return render(request, 'resources/resource_create_form.html', {'form':resource_form, 'type':type,} )
     
class EditLink(UpdatedActionMixin,generic.edit.UpdateView):
     model = Link
     form_class = LinkForm
     template_name='resources/resource_update_form.html'
     slug_field = 'slug'
     
class EditFile(UpdatedActionMixin,generic.edit.UpdateView):
     model = File
     form_class = FileForm
     template_name='resources/resource_update_form.html'
     slug_field = 'slug'
     
class EditPost(UpdatedActionMixin,generic.edit.UpdateView):
     model = Post
     form_class = PostForm
     template_name='resources/resource_update_form.html'
     slug_field = 'slug'
     
class ViewLink(generic.DetailView):
     model = Link
     template_name = 'resources/resource_detail.html'
     
class ViewFile(generic.DetailView):
     model = File
     template_name = 'resources/resource_detail.html'
     
class ViewPost(generic.DetailView):
     model = Post
     template_name = 'resources/post_detail.html'

class DeleteLink(MyDeleteMixin, generic.edit.DeleteView):

     model = Link
     success_url = reverse_lazy('resources')
     template_name = 'core/confirm_delete.html'
     
class DeleteFile(MyDeleteMixin, generic.edit.DeleteView):
     
     model = File
     success_url = reverse_lazy('resources')
     template_name = 'core/confirm_delete.html'
     
class DeletePost(MyDeleteMixin, generic.edit.DeleteView): #I'm pretty sure I can consolidate these delete views...
     
     model = Post
     success_url = reverse_lazy('resources')
     template_name = 'core/confirm_delete.html'
     
# REVIEW VIEWS -----------

# class AddReview(CreateActionMixin, generic.edit.CreateView):
#      model = Review
#      form_class = MyReviewForm
#      template_name='resources/review_form.html'
#      slug_field = 'slug'
     
def AddReview(request, slug):

     if request.method == 'POST':
          
          review_form = MyReviewForm(request.POST)
          
          if review_form.is_valid():
               new_review = review_form.save(commit=False)
               new_review.resource = Resource.objects.get(slug=slug)
               new_review.user = request.user
               new_review.save()
               messages.success(request,'Your review of \'%s\' has been saved.' % (new_review.resource))
               
               create_action(request.user, 'reviewed', new_review.resource)
               
               return redirect(new_review.resource)
     
     else:
          
          review_form = MyReviewForm()
          base_resource = Resource.objects.get(slug=slug)
          
     return render(request, 'resources/review_form.html',{'form':review_form,'resource':base_resource})
          
          

     
class EditReview(UpdatedActionMixin,generic.edit.UpdateView):
     model = Review
     form_class = MyReviewForm
     template_name='resources/review_form.html'
     slug_field = 'slug'
