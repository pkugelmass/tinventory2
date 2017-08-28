from django.http import HttpResponseRedirect
from django.contrib import messages
from people.helpers import create_action

class UpdatedActionMixin:
     
     def form_valid(self, form):
          updated_object = self.get_object()
          super(UpdatedActionMixin,self).form_valid(form)
          messages.success(self.request,'\'%s\' has been updated.' % (updated_object.title))
          create_action(self.request.user, 'updated', updated_object)
          return HttpResponseRedirect(self.get_success_url())
          
class CreateActionMixin:
     
     def form_valid(self, form):
        super(CreateActionMixin,self).form_valid(form)
        new_object = self.object
        messages.success(self.request,'Created \'%s\'.' % (new_object.title))
        create_action(self.request.user, 'created', new_object)
        return HttpResponseRedirect(self.get_success_url())