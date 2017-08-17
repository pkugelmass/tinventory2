from django.shortcuts import render
from .models import Topic
from django.views import generic
from resources.forms import LinkForm, AttachmentForm

class TopicsList(generic.ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    
    def get_queryset(self):
        return super(TopicsList,self).get_queryset().prefetch_related()
    
class TopicDetail(generic.DetailView):
    model = Topic
    template_name = 'topics/topic_detail.html'