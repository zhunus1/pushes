from django.core.management.base import BaseCommand, CommandError
from notifications.models import Event
from django.db.models import F
class Command(BaseCommand):
       def handle(self, *args, **options):
           events = Event.objects.filter(offset__lt=F('limit'))
           for event in events:
               print(event)
               #Run event
