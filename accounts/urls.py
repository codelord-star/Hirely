from django.urls import path
from .views import ProviderProfileView, my_customer_profile, register, ProtectedView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/customer-profile/', my_customer_profile, name='my_customer_profile'),
    path('provider/profile/', ProviderProfileView.as_view(), name='provider-profile'),
    path('test-protected/', ProtectedView.as_view(), name='test_protected'),
]