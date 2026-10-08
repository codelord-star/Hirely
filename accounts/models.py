from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Is email present?
        if not email:
            raise ValueError('Users must have an email address')

        # Normalize email
        email = self.normalize_email(email)

        # Construct User
        user = self.model(email=email, **extra_fields)
        # Hash password
        user.set_password(password)
        # Save user to database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        # Introducing the extra_fields dictionary to set default values for is_staff, is_superuser, and is_active
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # enforce is_staff and is_superuser to be True for superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True) #required=True is not required because Django fields are blank=False by default
    is_provider = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']    #this is for fields required when creating a superuser, since email is already required by default because it is the USERNAME_FIELD, we don't need to add it here

    def __str__(self):
        return self.email

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

