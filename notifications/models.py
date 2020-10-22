from django.db import models

class ServiceChoices(models.TextChoices):
    CARFAX = 'CFX','Carfax'
    ADVERTS = 'ADV','Adverts'
    APARKING = 'PRK','Aparking'
    GARAGE = 'GGG','Garage'

class Service(models.Model):
    service = models.CharField(
        max_length=3,
        choices=ServiceChoices.choices,
    )
    state = models.PositiveIntegerField(default=0)

class Event(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,default=None)
    reference_id = models.PositiveIntegerField()
    #FCM has 2 types of messages: 1)Notification message 2)Data message
    is_notification = models.BooleanField(default=True)
    data = models.JSONField()
    #Broadcast means deliver message to all users
    is_broadcast = models.BooleanField(default=False)
    offset = models.PositiveIntegerField(null=True,blank=True)
    limit = models.PositiveIntegerField(null=True,blank=True)
