from django.contrib import admin
from .models import Event,Service
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ('service', 'reference_id', 'send_at')
    list_filter = (
        'service',
    )
    search_fields = (
        'reference_id',
    )



admin.site.register(Event,EventAdmin)


class ServiceInline(admin.TabularInline):
    model = Event
    readonly_fields = ('created',)
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'state','url')
    inlines = [
        ServiceInline,
    ]
admin.site.register(Service,ServiceAdmin)
