from django.core.urlresolvers import reverse
from .forms import AttachmentForm, LinkForm


def resourceformfactory(resource_type, base, data, initial=False):
    
    if resource_type == 'file': form = AttachmentForm()
    if resource_type == 'link': form = LinkForm()
        
    if initial == True: form.initial = data
    #if initial == False: form = form
    
    return form

def viewthisresource(resource_object):
    
    if resource_object.type == 'File':
        return reverse('view-file', pk=resource_object.pk)
    
    if resource_object.type == 'Link':
        return reverse('view-link', pk=resource_object.pk)