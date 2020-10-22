from django.urls import path
from .views import EventViewSet,DeviceViewSet,SendMessageViewSet
from . import views
app_name = 'notifications'

urlpatterns = [
    path('event/',EventViewSet.as_view()),
    path('device/',DeviceViewSet.as_view()),
    path('send/',SendMessageViewSet.as_view()),
]
