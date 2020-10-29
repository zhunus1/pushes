from rest_framework import serializers
from fcm_django.models import FCMDevice
from .models import Event,Service
from users.models import DuplicateUser

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = '__all__'

    def create(self,validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['name'] = user.first_name
        return FCMDevice.objects.create(**validated_data)


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    state = serializers.IntegerField()
    class Meta:
        model = Event
        fields = ['send_at','reference_id', 'data', 'is_broadcast']

class RetrievedEventSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    class Meta:
        model = Event
        fields = ['send_at','pk', 'data', 'is_broadcast']

class EventDetailSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    listeners = serializers.ListField(
         child=serializers.IntegerField()
    )
    class Meta:
        model = Event
        fields = ['send_at','pk', 'data', 'is_broadcast','listeners']



# class NotificationSerializer(serializers.Serializer):
#     user_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         )
#     event = EventSerializer()
