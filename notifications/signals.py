from django.db.models.signals import post_save,post_delete
from notifications.models import Event,Service
from users.models import DuplicateUser
from fcm_django.models import FCMDevice

from django.dispatch import receiver
from django_q.tasks import schedule
from urllib import request

# @receiver(post_save,sender=Event)
# def save_event(sender,instance:Event,**kwargs):
#     service = Service.objects.filter(service=instance.service).first()
#     service.state+=1
#     service.save()

def task(service,sender):
    response = requests.get(service.url,params={'pk':sender.pk},timeout=60)
    event_data = response.json()
    listeners = event_data['listeners']
    users = DuplicateUser.objects.filter(caps_id__in=listeners)
    devices = FCMDevice.objects.filter(user__in=users)
    devices.send_message(title=event_data.title, body=event_data.body)

#Need to check state. See user manual

@receiver(post_save,sender=Event)
def start_tasks(sender,instance:Event,**kwargs):
    service = Service.objects.filter(service=instance.service)
    service.state+=1
    service.save()
    schedule('task',
             service, sender,
             hook=None,
             schedule_type=Schedule.DAILY)

@receiver(post_delete,sender=Service)
def delete_tasks(sender,instance:Event,**kwargs):
    
    return None
