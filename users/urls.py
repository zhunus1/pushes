from django.urls import path
from .views import (
    AuthTokenAPIView,
    ProfileAPIView,
    sync_view,
    # upload_avatar,
    # remove_avatar,
)


app_name = 'users'

urlpatterns = [
    path('token/', AuthTokenAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('sync/', sync_view),
]
