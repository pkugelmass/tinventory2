from django.shortcuts import render
from .models import Topic
from django.views import generic

class TopicsList(generic.ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    
class TopicDetail(generic.DetailView):
    model = Topic
    template_name = 'topics/topic_detail.html'
    # slug_field = 'title'