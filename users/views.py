import os
import uuid
import requests
import logging
from io import StringIO, BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .models import (
    DuplicateUser,
)

from .authentication import FastAuthentication

from .serializers import (
    AuthSerializer,
    ProfileSerializer,
    UploadImageSerializer,
)

# Create your views here.


class AuthTokenAPIView(APIView):

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = FastAuthentication \
            .get_user_from_caps_token(serializer.validated_data['token'])

        if user is not None:
            serializer = AuthSerializer({
                'token': FastAuthentication.get_token_from_user(user)
            })
            return Response(serializer.data)
        else:
            logging.error(serializer.errors)
            return Response({'status': 'Invalid token'},
                    status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(APIView):

    authentication_classes = (FastAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.pop('token', None)

        if 'birthday' in serializer.validated_data:
            serializer.validated_data['date_of_birth'] = \
                serializer.validated_data.pop('birthday', None)

        response = requests.put(
            '%s/api/users/profile/' % settings.CAPS_URL,
            json=serializer.validated_data,
            headers={'Authorization': 'Token %s' % token, 'Host': settings.CAPS_HOST},
            timeout=1,
        )

        if status.is_success(response.status_code):
            data = response.json()
            user = request.user

            if data['id'] == user.caps_id:
                # user.phone_number = data['phone']
                user.email = data['email']
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.avatar = data['profile_avatar_url']
                user.thumbnail = data['profile_avatar_thumbnail_url']
                user.birthday = data['date_of_birth']
                user.gender = data['gender']
                user.save()
                return Response(ProfileSerializer(user).data)
            else:
                raise NotAuthenticated()

        data = response.json()
        if 'date_of_birth' in data:
            data['birthday'] = data.pop('date_of_birth', None)
        return Response(data, status=response.status_code)


@api_view(['POST'])
@authentication_classes([FastAuthentication])
@permission_classes([IsAuthenticated])
def sync_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = serializer.validated_data['token']

    response = requests.get(
        '%s/api/users/profile/' % settings.CAPS_URL,
        headers={'Authorization': 'Token %s' % token, 'Host': settings.CAPS_HOST},
        timeout=1,
    )

    if status.is_success(response.status_code):
        data = response.json()
        user = request.user

        if data['id'] == user.caps_id:
            user.phone_number = data['phone']
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.avatar = data['profile_avatar_url']
            user.thumbnail = data['profile_avatar_thumbnail_url']
            user.birthday = data['date_of_birth']
            user.gender = data['gender']['value']
            user.save()
            data['gender'] = data['gender']['value']
            return Response(ProfileSerializer(user).data)
        else:
            raise NotFound()

    return Response(response.json(), status=response.status_code)
