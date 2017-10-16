from django.shortcuts import render
from django.http import HttpResponse
from .models import Transformation, Ministry
from .forms import TransformationFilterForm, TransformationForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from people.viewmixins import UpdatedActionMixin, CreateActionMixin
from django.db.models import Q 

# GENERAL MIXINS

class MyDeleteMixin:
     success_message = "Delete successful."
     
     def delete(self, request, *args, **kwargs):
          messages.success(self.request, self.success_message)
          return super(generic.edit.DeleteView, self).delete(request, *args, **kwargs)
     

# LIST/HOME VIEW

def IndexView(request):
     
     form = TransformationFilterForm()
     query_set = Transformation.objects.all()
     
     if request.GET:
          
          q_list = []
          
          if request.GET['ministry'] != '': q_list = q_list + [Q(ministry__abbrev=request.GET['ministry'])]
          if request.GET['category'] != '': q_list = q_list + [Q(category=request.GET['category'])]
          if request.GET['status'] != '': q_list = q_list + [Q(status=request.GET['status'])]
          if request.GET['tags'] != '': q_list = q_list + [Q(tags__name=request.GET['tags'])]
          
          if len(q_list) > 0: # Only if there is something to filter...
               
               combined_q = Q(pk__gt=0) # Initialize a blank combined query.
               
               while len(q_list) > 0:
                    combined_q &= q_list.pop()
               query_set = query_set.filter(combined_q) # Filter resources by the combined query.
               
          # Set the forms to show the criteria used when they are reloaded.
          for fieldname in request.GET:
               form.fields[fieldname].initial = request.GET[fieldname]

     package = {
          'transformation_list' : query_set,
          't_filter_form' : form,
          }
     
     return render(request, 'transformations/index.html', package)
     
# TRANSFORMATION DETAIL VIEWS AND FORMS

class TransformationFormMixin:
     model = Transformation
     form_class = TransformationForm

class TransformationDetail(generic.DetailView):
     model = Transformation

class AddTransformation(CreateActionMixin, TransformationFormMixin, generic.edit.CreateView):
     pass
     
class EditTransformation(UpdatedActionMixin, generic.edit.UpdateView):
     model = Transformation
     form_class = TransformationForm
     
     
class DeleteTransformation(MyDeleteMixin, generic.edit.DeleteView):
     model = Transformation
     success_url = reverse_lazy('index')
     template_name = 'core/confirm_delete.html'