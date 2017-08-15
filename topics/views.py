from django.shortcuts import render
from .models import Topic
from django.views import generic

class TopicsList(generic.ListView):
    model = Topic
    template_name = 'topics/topics_list.html'