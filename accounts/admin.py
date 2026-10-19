from django.contrib import admin
from .models import CustomerProfile, ProviderProfile, User

# Register your models here.
admin.site.register(User)
admin.site.register(CustomerProfile)
admin.site.register(ProviderProfile)
