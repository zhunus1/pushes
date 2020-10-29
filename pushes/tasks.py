from django_q.tasks import schedule

from notifications.models import Event
from rest_framework import status

from notifications.serializers import RetrievedEventSerializer

import requests

from notifications.models import Service,Event
from django.db import transaction
from django.db.models.signals import post_save


def get_events(service,remote_state):
    offset = service.state
    limit = remote_state - service.state
    response = requests.get(service.url,params={'limit':limit,'offset':offset},timeout=60,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
    if status.is_success(response.status_code):
        data = response.json()
        events = []
        for event in data['results']:
            serializer = RetrievedEventSerializer(data=event)
            serializer.is_valid(raise_exception=True)
            events.append(Event(
                service = service,
                send_at = serializer.validated_data['send_at'],
                reference_id = serializer.validated_data['pk'],
                data = serializer.validated_data['data'],
                is_broadcast = serializer.validated_data['is_broadcast'],
            ))
        Event.objects.bulk_create(events)
        for event in events:
            post_save.send(sender=Event, instance=event, created=True)
        service.state+=len(events)
        service.save()



def check_state(service):
    response = requests.get('http://192.168.100.72:8002/ru/notifications/state/',timeout=5,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
    if status.is_success(response.status_code):
        data = response.json()
        local_service = Service.objects.get(service=service)
        if local_service.state < data['state']:
            get_events(local_service,data['state'])
