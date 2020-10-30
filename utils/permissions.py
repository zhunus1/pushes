from django.conf import settings
from rest_framework import permissions

class IsService(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get('x-api-key')
        return settings.COMMON_API_KEY == token
