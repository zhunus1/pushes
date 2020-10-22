from rest_framework import serializers
from fcm_django.models import FCMDevice
from .models import Event,Service

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Event
        fields = ['service', 'reference_id', 'is_notification', 'data', 'is_broadcast']
