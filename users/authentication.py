import json

import requests

from django.conf import settings

from django.utils import timezone

from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from utils.encryption import encrypt, decrypt

from django.core.exceptions import ObjectDoesNotExist

from .models import DuplicateUser


class FastAuthentication(BaseAuthentication):

    TOKEN_PREFIX = 'FastToken'
    model = None

    @staticmethod
    def get_token_from_user(user):
        data = {
            'user_id': user.pk,
            'created': str(timezone.now()),
        }
        b = json.dumps(data)
        token = encrypt(b.encode().hex(), settings.SECRET_KEY)
        return token

    @staticmethod
    def get_user_from_token(token):
        try:
            payload = bytes.fromhex(decrypt(token, settings.SECRET_KEY))
            data = json.loads(payload)
            user = DuplicateUser.objects.get(pk=data['user_id'])
            return user
        except Exception:
            return None

    @staticmethod
    def get_user_from_caps_token(caps_token):

        # TODO: remote call with Shared Key
        response = requests.get(
            '%s/api/users/profile/' % settings.CAPS_URL,
            headers={'Authorization': 'Token %s' % caps_token, 'Host': settings.CAPS_HOST},
            timeout=1,
        )

        if status.is_success(response.status_code):
            data = response.json()
            caps_id = data.get('id')
            if caps_id is not None:
                user, created = DuplicateUser.objects.get_or_create(caps_id=caps_id, defaults={
                    'caps_id': data['id'],
                    'phone_number': data['phone'],
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'avatar': data['profile_avatar_url'],
                    'thumbnail': data['profile_avatar_thumbnail_url'],
                    'birthday': data['date_of_birth'],
                    'gender': data['gender']['value'],
                    'caps_token' : caps_token,
                })
                if not created:
                    user.phone_number = data['phone']
                    user.email = data['email']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.avatar = data['profile_avatar_url']
                    user.thumbnail = data['profile_avatar_thumbnail_url']
                    user.birthday = data['date_of_birth']
                    user.gender = data['gender']['value']
                    user.caps_token = caps_token
                    user.save()
                return user
        return None

    def authenticate(self, request):
        try:
            auth = get_authorization_header(request).decode().split()

            if not auth or auth[0] != FastAuthentication.TOKEN_PREFIX:
                return None

            user = FastAuthentication.get_user_from_token(auth[1])
            if user is not None:
                return user, auth[1]
            return None
        except Exception as e:
            return None
