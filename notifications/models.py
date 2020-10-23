from django.db import models
from datetime import datetime

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
    url = models.URLField()#ssylka na service po kotoroi ya budu dostavat' eventy
    #Signal na post_save post_delete
    def __str__(self):
        return self.service

class Event(models.Model):
    send_at = models.DateTimeField(blank=True,null=True)#if Null then send Immeaditely
        #If data is passed then send Immeaditely
        #Filter by NUll and Date by asc dates[] which I accept from Service
    reference_id = models.PositiveIntegerField()
    #FCM has 2 types of messages: 1)Notification message 2)Data message
    is_notification = models.BooleanField(default=True)
    data = models.JSONField()
    #Broadcast means deliver message to all users
    is_broadcast = models.BooleanField(default=False)
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="Updated",
        auto_now=True,
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.reference_id)
