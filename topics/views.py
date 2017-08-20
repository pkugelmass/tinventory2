from django.shortcuts import render
from .models import Topic
from django.views import generic
from resources.forms import LinkForm, FileForm

class TopicsList(generic.ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    
    def get_queryset(self):
        return super(TopicsList,self).get_queryset().prefetch_related()
    
def TopicDetail(request, slug):
    
    this_topic = Topic.objects.get(slug=slug)
    
    context = {
        'topic':this_topic,
        }
        
    return render(request,'topics/topic_detail.html',context)