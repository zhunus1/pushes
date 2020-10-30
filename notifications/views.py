from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.authentication import FastAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import transaction

import requests

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .models import Event,Service
from users.models import DuplicateUser
from fcm_django.models import FCMDevice
from .serializers import EventSerializer,DeviceSerializer,EventDetailSerializer
from users.serializers import ProfileSerializer
from utils.permissions import IsService

from urllib.parse import urljoin


#Creates device for particular user
#Called from front-end by user's phone when entering application
class DeviceViewSet(APIView):
    authentication_classes = (FastAuthentication,)
    permission_classes = (
        IsAuthenticated,
        )

    def post(self,request,format=None):
        context = {'request': self.request}
        serializer = DeviceSerializer(data=request.data,context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Creates Event
class EventViewSet(APIView):
    permission_classes = (IsService,)

    def post(self,request,service,format=None):
        data = request.data
        service = Service.objects.get(service=service)
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        remote_state = serializer.validated_data['state']
        current_state = service.state + 1
        if current_state == remote_state:
            url = urljoin(service.url,(str(serializer.validated_data['reference_id'])+'/'))
            response = requests.get(url,timeout=5,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
            if status.is_success(response.status_code):
                data = response.json()
                serializer = EventDetailSerializer(data=data)
                if serializer.is_valid():
                    Event.objects.create(
                        service = service,
                        send_at = serializer.validated_data['send_at'],
                        reference_id = serializer.validated_data['pk'],
                        data = serializer.validated_data['data'],
                        is_broadcast = serializer.validated_data['is_broadcast']
                    )
                service.state+=1
                service.save()
        else:
            offset = service.state
            limit = remote_state - service.state
            response = requests.get(service.url,params={'limit':limit,'offset':offset},timeout=60,headers={'X-API-KEY':'85cb29a1-c630-496b-949d-8f9a1b8b7306'})
            if status.is_success(response.status_code):
                data = response.json()
                events = []
                with transaction.atomic():
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

        return Response(serializer.data,status=status.HTTP_201_CREATED)



# class SendMessageViewSet(APIView):
#     #authentication_classes  = Custom authorization needed X-API-KEY?
#
#     def post(self,request,format=None,**kwargs):
#         service = kwargs.get('service')
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             #Check for service
#             service = kwargs['service']
#             print(service)
#             #Increment state when executing Event
#             #Save event according to service name
#
#
#             # user_caps_ids = serializer.validated_data['user_ids']
#             # users = DuplicateUser.objects.filter(caps_id__in=user_caps_ids)
#             # devices = FCMDevice.objects.filter(user__in=users)
#             #devices.send_message(title="Nursultan!", body="Salamaleikum!")
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
