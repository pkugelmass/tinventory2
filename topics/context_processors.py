from .models import Topic

def add_topics(request):
    topics_list = Topic.objects.filter(level=0)
    return {'topics':topics_list}