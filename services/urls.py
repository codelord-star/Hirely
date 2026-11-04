from django.urls import path

from .views import PublicServiceDetailView, PublicServiceView, create_service, get_service, list_categories, update_service, my_services, delete_service

urlpatterns = [
    # provider crud functions
    path('create/', create_service, name='create_service'),
    path('<int:service_id>/update/', update_service, name='update_service'),
    path('my-services/', my_services, name='my_services'),
    path('my-services/<int:service_id>/', get_service, name='get_service'),
    path('<int:service_id>/delete/', delete_service, name='delete_service'),
    path('categories/', list_categories, name='list_categories'),

    # customer view functions
    path('', PublicServiceView.as_view(), name='public_services'),
    path('<int:service_id>/', PublicServiceDetailView.as_view(), name='public_service_detail'),
]