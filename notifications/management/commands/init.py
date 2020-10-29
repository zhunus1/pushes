from django.core.management.base import BaseCommand, CommandError
from notifications.models import Event
from django.db.models import F

from django_q.models import Schedule
from django_q.tasks import schedule

import math
class Command(BaseCommand):
       def handle(self, *args, **options):
           pass
