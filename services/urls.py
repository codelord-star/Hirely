from django.urls import path

from .views import create_service, update_service, my_services, delete_service

urlpatterns = [
    path('create/', create_service, name='create_service'),
    path('<int:service_id>/update/', update_service, name='update_service'),
    path('my-services/', my_services, name='my_services'),
    path('<int:service_id>/delete/', delete_service, name='delete_service'),
]