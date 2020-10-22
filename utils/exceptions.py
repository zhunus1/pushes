from django.utils.translation import *
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):

    status_code = 503
    default_detail = ugettext_lazy("Service temporarily unavailable, try again later.")
    default_code = 'service_unavailable'


class CloudpaymentsException(Exception):

    code = -1

    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code


class DateException(Exception):

    pass


class IntegrityException(Exception):

    pass
