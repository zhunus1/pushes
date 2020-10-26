from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.authentication import FastAuthentication
from rest_framework import status
from rest_framework.decorators import api_view

from urllib import request

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .models import Event,Service
from users.models import DuplicateUser
from fcm_django.models import FCMDevice
from .serializers import EventSerializer,DeviceSerializer
from users.serializers import ProfileSerializer


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
    #authentication_classes  = Custom authorization needed X-API-KEY?

    def post(self,request,format=None,**kwargs):
        serializer = EventSerializer(data=request.data)
        service_name = kwargs.get('service')
        service = Service.objects.get(service=service_name)
        serializer.is_valid(raise_exception=True)
        state = serializer.validated_data['state']
        if service.state + 1 == state:
            service.state+=1
            service.save()
            serializer.save()
        elif service.state < state:
            #call api lacks time
            limit = state - service.state
            offset = service.state
            response = requests.get(service.url,params={'limit':limit,'offset':offset},timeout=60)
            if status.is_success(response.status_code):
                data = response.json()
                sz = EventSerializer(data=data, many=True)
                sz.is_valid(raise_exception=True)
                event_list = []
                for event_data in sz.validated_data:
                    event_list.append(Event(**event_data))
                Event.objects.bulk_create(event_list)
                return Response(sz.data, status=status.HTTP_201_CREATED)
            else:
                return Response(response.json(), response.status_code)
        else:
            return Response(status=status.HTTP_201_CREATED)

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
