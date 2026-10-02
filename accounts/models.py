from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)