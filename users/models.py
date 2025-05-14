from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gender = models.CharField(max_length=50, blank=True)
    skin_tone = models.CharField(max_length=50, blank=True)
    eye_color = models.CharField(max_length=50, blank=True)
    hair_color = models.CharField(max_length=50, blank=True)
    height = models.IntegerField() 
    Weight = models.IntegerField() 
    firebase_id = models.CharField(max_length=100) 