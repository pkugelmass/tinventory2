from django.shortcuts import redirect
from .forms import FileForm, LinkForm, PostForm


def resourceformfactory(resource_type, base, data, files=None, initial=False):
    
    if initial == False:
        if resource_type == 'file': form = FileForm(data, files)
        if resource_type == 'link': form = LinkForm(data)
        if resource_type == 'post': form = PostForm(data)
    if initial == True:
        if resource_type == 'file': form = FileForm(initial=data)
        if resource_type == 'link': form = LinkForm(initial=data)
        if resource_type == 'post': form = PostForm(initial=data)
    
    return form

def viewthisresource(resource_object):
    
    if resource_object.type == 'file':
        return redirect('view-file', slug=resource_object.slug)
    
    if resource_object.type == 'link':
        return redirect('view-link', slug=resource_object.slug)
        
    if resource_object.type == 'post':
        return redirect('view-post', slug=resource_object.slug)