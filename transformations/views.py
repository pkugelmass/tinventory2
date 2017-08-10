from django.shortcuts import render
from django.http import HttpResponse
from .models import Transformation, Ministry
from .forms import TransformationFilterForm, TransformationForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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
          
          # Format the input into keyword arguments (eg. category:structure)
          criteria = { a.lower():request.GET[a] for a in request.GET if request.GET[a] != ''}
          
          # Filter the query based on those arguments (if any).
          query_set = query_set.filter(**criteria).prefetch_related('ministry')
          
          # Set the forms to show the criteria used when they are reloaded.
          for fieldname in criteria:
               form.fields[fieldname].initial = criteria[fieldname]

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

class AddTransformation(SuccessMessageMixin, TransformationFormMixin, generic.edit.CreateView):
     success_message = "Transformation created."
     
class EditTransformation(SuccessMessageMixin, generic.edit.UpdateView):
     model = Transformation
     form_class = TransformationForm
     success_message = "Transformation updated."
     
     # def form_valid(self,form):
     #      messages.success(self.request,'Transformation updated.')
     #      return super(EditTransformation,self).form_valid(form)
     
     
class DeleteTransformation(MyDeleteMixin, generic.edit.DeleteView):
     model = Transformation
     success_url = reverse_lazy('index')
     template_name = 'core/confirm_delete.html'