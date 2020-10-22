from rest_framework import serializers

from .models import (
    DuplicateUser,
)

class AuthSerializer(serializers.Serializer):

    token = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):

    token = serializers.CharField(write_only=True)

    class Meta:

        model = DuplicateUser
        fields = (
            'pk',
            'caps_id',
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'thumbnail',
            'birthday',
            'last_seen',
            'gender',
            'is_manager',
            'token',
        )
        read_only_fields = (
            'caps_id',
        )


class UploadImageSerializer(serializers.Serializer):

    token = serializers.CharField(write_only=True)
    original = serializers.ImageField()
    thumbnail = serializers.ImageField()
