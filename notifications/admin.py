from django.contrib import admin
from .models import Event,Service
# Register your models here.
admin.site.register(Event)
admin.site.register(Service)

class EventAdmin(admin.ModelAdmin):
    # list_display = (
    #     '__str__',
    #     'user',
    #     'vin',
    #     'include_dtp',
    #     'include_reg',
    #     'dtp_checksum',
    #     'reg_checksum',
    #     'transaction_id',
    #     'previous_report',
    #     'created',
    #     'updated',
    # )
    # readonly_fields = (
    #     'include_dtp',
    #     'include_reg',
    #     'dtp_checksum',
    #     'reg_checksum',
    #     'transaction_id',
    #     'previous_report',
    #     'created',
    #     'updated',
    # )
    # list_filter = (
    #     'include_dtp',
    #     'include_reg',
    # )
    # search_fields = (
    #     'user__caps_id',
    #     'user__phone_number',
    #     'user__email',
    #     'user__first_name',
    #     'user__last_name',
    #     'vin',
    # )
    date_hierarchy = 'created'
