from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from people.models import Profile

class SetLastVisitMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            Profile.objects.filter(user=request.user).update(last_login=now())
        return response