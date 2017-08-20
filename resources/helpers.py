from django.shortcuts import redirect
from .forms import FileForm, LinkForm


def resourceformfactory(resource_type, base, data, files=None, initial=False):
    
    if initial == False:
        if resource_type == 'file': form = FileForm(data, files)
        if resource_type == 'link': form = LinkForm(data)
    if initial == True:
        if resource_type == 'file': form = FileForm(initial=data)
        if resource_type == 'link': form = LinkForm(initial=data)
    
    return form

def viewthisresource(resource_object):
    
    if resource_object.type == 'File':
        return redirect('view-file', slug=resource_object.slug)
    
    if resource_object.type == 'Link':
        return redirect('view-link', slug=resource_object.slug)