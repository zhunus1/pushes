from django.db.models.signals import post_save,post_delete
from notifications.models import Event,Service
from users.models import DuplicateUser
from fcm_django.models import FCMDevice
from django_q.models import Schedule

from rest_framework import status
from django.dispatch import receiver
from django_q.tasks import schedule
import requests
from .serializers import EventDetailSerializer
from urllib.parse import urljoin
from django.forms.models import model_to_dict
from django.utils import timezone

from django_q.tasks import async_task
# @receiver(post_save,sender=Event)
# def save_event(sender,instance:Event,**kwargs):
#     service = Service.objects.filter(service=instance.service).first()
#     service.state+=1
#     service.save()

def broadcast(data):
    devices = FCMDevice.objects.all()
    devices.send_message(title=data['title'], body=data['body'])

def multicast(listeners,data):
    users = DuplicateUser.objects.filter(caps_id__in=listeners)
    devices = FCMDevice.objects.filter(user__in=users)
    devices.send_message(title=data['title'], body=data['body'])

@receiver(post_save,sender=Event)
def start_tasks(sender,instance:Event,**kwargs):
    service = instance.service
    url = urljoin(service.url,(str(instance.reference_id)+'/'))
    response = requests.get(url,timeout=5,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
    if status.is_success(response.status_code):
        event_data = response.json()
        serializer = EventDetailSerializer(data=event_data)
        serializer.is_valid(raise_exception=True)

        is_broadcast = serializer.validated_data['is_broadcast']
        if serializer.validated_data['send_at'] > timezone.now():
            if is_broadcast:
                schedule('notifications.signals.broadcast',
                         serializer.validated_data['data'],
                         schedule_type=Schedule.ONCE,
                         repeats = 1,
                         next_run=serializer.validated_data['send_at'])
            else:
                schedule('notifications.signals.multicast',
                        serializer.validated_data['listeners'],serializer.validated_data['data'],
                        schedule_type=Schedule.ONCE,
                        repeats = 1,
                        next_run=serializer.validated_data['send_at'])
        else:
            if is_broadcast:
                async_task('notifications.signals.broadcast',serializer.validated_data['data'])
            else:
                async_task('notifications.signals.multicast',serializer.validated_data['listeners'],serializer.validated_data['data'])


#Need to check state. See user manual

@receiver(post_save,sender=Service)
def start_check(sender,instance:Service,created,**kwargs):
    if created:
        schedule('pushes.tasks.check_state',
                 instance.service,
                 schedule_type=Schedule.MINUTES,
                 repeats=-1,
                 name=instance.service,)

@receiver(post_delete,sender=Service)
def delete_tasks(sender,instance:Service,**kwargs):
    Schedule.objects.filter(name=instance.service).delete()
