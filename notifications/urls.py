from django.urls import path
from .views import EventViewSet
from . import views
app_name = 'notifications'

urlpatterns = [
    path('event/',EventViewSet.as_view()),
]
