from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True) #required=True is not required because Django fields are blank=False by default
    is_provider = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    #this is for fields required when creating a superuser, since email is already required by default because it is the USERNAME_FIELD, we don't need to add it here

    def __str__(self):
        return self.email


