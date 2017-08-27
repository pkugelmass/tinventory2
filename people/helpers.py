from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone
from django.contrib import messages

def create_action(user, verb, target=None):
    
    # Check if a similar action has been created in the past minute.
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,verb=verb, created__gte=last_minute)
    
    if target:
        target_type = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_type=target_type, target_id=target.id)
        
    # If no similar action has been created, record a new action.
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
        
    return False