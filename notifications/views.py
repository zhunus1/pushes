from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.authentication import FastAuthentication
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .models import Event
from users.models import DuplicateUser
from fcm_django.models import FCMDevice
from .serializers import EventSerializer,DeviceSerializer,MessageSerializer
from users.serializers import ProfileSerializer

#Creates Event
class EventViewSet(APIView):
    authentication_classes = (FastAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )
    def post(self,request,format=None):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Creates device for particular user
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

class SendMessageViewSet(APIView):
    #authentication_classes  = Custom authorization needed

    def post(self,request,format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            #STATE NUMBER NEEDED
            user_caps_ids = serializer.validated_data['user_ids']
            users = DuplicateUser.objects.filter(caps_id__in=user_caps_ids)
            devices = FCMDevice.objects.filter(user__in=users)
            devices.send_message(title="Title", body="Message")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
