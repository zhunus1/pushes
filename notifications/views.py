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

from fcm_django.models import FCMDevice
from .serializers import EventSerializer,DeviceSerializer

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
