from django.db import models

class ChoicesManager(models.Manager):
     def choices_list(self):
          return ( ( m , m.long() ) for m in self.get_queryset() )