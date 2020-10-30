from django.urls import path
from .views import EventViewSet,DeviceViewSet
from . import views
app_name = 'notifications'

urlpatterns = [
    path('event/<str:service>',EventViewSet.as_view()),
    path('device/register',DeviceViewSet.as_view()),
]
