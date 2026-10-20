from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import ProviderProfile

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name


class Service(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='services')

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
    price_ksh = models.DecimalField(max_digits=10, decimal_places=2)

    PRICING_TYPE_CHOICES = [
        ("Fixed", "Fixed"),
        ("Hourly", "Hourly"),
        ("Per Project", "Per Project"),
        ("Negotiable", "Negotiable"),
        # ("Subscription", "Subscription"),
    ]

    pricing_type = models.CharField(max_length=50, choices=PRICING_TYPE_CHOICES)
    service_image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    duration_min = models.PositiveIntegerField(blank=True, null=True)
    duration_max = models.PositiveIntegerField(blank=True, null=True)

    DURATION_UNIT_CHOICES = [
        ("Minutes", "Minutes"),
        ("Hours", "Hours"),
        ("Days", "Days"),
        ("Weeks", "Weeks"),
    ]

    duration_unit = models.CharField(max_length=20, choices=DURATION_UNIT_CHOICES, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.duration_min is not None and self.duration_max is not None:
            if self.duration_min > self.duration_max:
                raise ValidationError("Minimum duration cannot be greater than maximum duration.")

        if self.duration_min is not None or self.duration_max is not None:
            if not self.duration_unit:
                raise ValidationError("Duration unit must be specified if duration is provided.")

        if self.duration_min is not None and self.duration_min <= 0:
            raise ValidationError("Minimum duration must be greater than zero.")

        if self.duration_max is not None and self.duration_max <= 0:
            raise ValidationError("Maximum duration must be greater than zero.")

        if (self.duration_min is None and self.duration_max is None and self.duration_unit):
            raise ValidationError("Duration unit cannot be provided without a duration value.")

    def __str__(self):
        return f"{self.provider.business_name} - {self.title}"