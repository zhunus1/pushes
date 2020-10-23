from django.db.models.signals import post_save
from notifications.models import Event,Service
from django.dispatch import receiver

# @receiver(post_save,sender=Event)
# def save_event(sender,instance:Event,**kwargs):
#     service = Service.objects.filter(service=instance.service).first()
#     service.state+=1
#     service.save()
