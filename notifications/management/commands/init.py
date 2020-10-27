from django.core.management.base import BaseCommand, CommandError
from notifications.models import Event
from django.db.models import F

from django_q.models import Schedule
from django_q.tasks import schedule

import math
class Command(BaseCommand):
       def handle(self, *args, **options):
           # Schedule.objects.create(func='check_state',
           #                         args='Carfax',
           #                         schedule_type=Schedule.MINUTES,
           #                         minutes=1
           #                         )
           schedule('pushes.tasks.check_state',
                     'CFX',
                     schedule_type=Schedule.MINUTES)
