from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date

class User(AbstractUser):
    class user_status(models.TextChoices):
        UNVERIFIED = 'unverified', 'Unverified'
        VERIFIED = 'verified', 'Verified'
        SUSPENDED = 'suspended', 'Suspended'
        DELETED = 'deleted', 'Deleted'
    
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=15, choices=user_status.choices, default=user_status.UNVERIFIED)
    
    is_active = models.BooleanField(default=True)

    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def __str__(self):
        return self.username
