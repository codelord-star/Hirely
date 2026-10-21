from django.urls import path

from .views import create_service

urlpatterns = [
    path('create/', create_service, name='create_service'),
]