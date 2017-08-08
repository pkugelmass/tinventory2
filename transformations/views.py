from django.shortcuts import render
from django.http import HttpResponse
from .models import Transformation, Ministry, Attachment, Link
from .forms import TransformationFilterForm, TransformationForm, LinkForm, AttachmentForm
from django.views import generic
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse

# LIST/HOME VIEW

def IndexView(request):
     
     form = TransformationFilterForm()
     query_set = Transformation.objects.all()
     
     if request.GET:
          
          # Format the input into keyword arguments (eg. category:structure)
          criteria = { a.lower():request.GET[a] for a in request.GET if request.GET[a] != ''}
          
          # Filter the query based on those arguments (if any).
          query_set = query_set.filter(**criteria)
          
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

class AddTransformation(TransformationFormMixin, generic.edit.CreateView):
     pass
     
class EditTransformation(TransformationFormMixin, generic.edit.UpdateView):
     pass
     
class DeleteTransformation(generic.edit.DeleteView):
     model = Transformation
     success_url = reverse_lazy('index')
     
# FILE MGMT VIEWS AND FORMS

class ResourceFormMixin:
     template_name='transformations/resource_form.html'
     
     def get_initial(self):
          initial = super(generic.edit.CreateView, self).get_initial()
          try:
               initial['transformation'] = Transformation.objects.get(pk=self.kwargs['tID'])
          except:
               pass
          return initial
          
class AddLink(ResourceFormMixin, generic.edit.CreateView):
     model = Link
     form_class = LinkForm
     
class AddFile(ResourceFormMixin, generic.edit.CreateView):
     model = Attachment
     form_class = AttachmentForm
     
class EditLink(generic.edit.UpdateView):
     model = Link
     form_class = LinkForm
     template_name='transformations/resource_form.html'
     
class EditFile(generic.edit.UpdateView):
     model = Attachment
     form_class = AttachmentForm
     template_name='transformations/resource_form.html'
     
class ViewLink(generic.DetailView):
     model = Link
     template_name = 'transformations/resource_detail.html'
     
class ViewFile(generic.DetailView):
     model = Attachment
     template_name = 'transformations/resource_detail.html'

class DeleteLink(generic.edit.DeleteView):

     def get_success_url(self):
          # Assuming there is a ForeignKey from Comment to Post in your model
          transformation = self.object.transformation
          return reverse_lazy( 'transformation-detail', kwargs={'pk': transformation.pk})

     model = Link
     success_url = reverse_lazy('index')
     template_name = 'transformations/transformation_confirm_delete.html'
     

     
class DeleteFile(generic.edit.DeleteView):
     
     def get_success_url(self):
          # Assuming there is a ForeignKey from Comment to Post in your model
          transformation = self.object.transformation
          return reverse_lazy( 'transformation-detail', kwargs={'pk': transformation.pk})
     
     model = Attachment
     # success_url = reverse_lazy('index')
     template_name = 'transformations/transformation_confirm_delete.html'