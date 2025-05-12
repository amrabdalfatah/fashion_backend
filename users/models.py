from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    skin_tone = models.CharField(max_length=50, blank=True)
    eye_color = models.CharField(max_length=50, blank=True)
    body_measurements = models.JSONField(default=dict)  # Stores {height, bust, waist, hip}
    firebase_id = models.CharField(max_length=100) 