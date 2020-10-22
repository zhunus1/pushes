from rest_framework.utils.encoders import JSONEncoder
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber


class AdvancedJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, PhoneNumber):
            return str(obj)
        return super().default(obj)
