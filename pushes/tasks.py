from django_q.tasks import schedule

from notifications.models import Event
from rest_framework import status

from notifications.serializers import RetrievedEventSerializer

import requests
import urllib

from notifications.models import Service,Event


def send_notification(service_name):
    service = Service.objects.get(service=service_name)
    response_state = requests.get(urllib.parse.urljoin(service.url,'state/'),timeout=1)
    data_state = response_state.json()
    offset = service.state
    limit = data_state['state'] - service.state
    response = requests.get(service.url,params={'limit':limit,'offset':offset},timeout=10)
    if status.is_success(response.status_code):
        data = response.json()
        serializer = RetrievedEventSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        events = []
        for event in serializer.validated_data:
            events.append(Event(**event))
        Event.objects.bulk_create(events)




def check_state(service_name):
    service = Service.objects.get(service=service_name)
    response = requests.get('http://192.168.100.72:8002/ru/notifications/state/',timeout=5,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
    if status.is_success(response.status_code):
        data = response.json()
        if service.state < data['state']:
            send_notification(service_name)
        else:
            pass
    else:
        return response.status_code
