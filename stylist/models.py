from django.db import models

# Create your models here.
class OutfitRecommendation(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    occasion = models.CharField(max_length=100)  # e.g., "wedding", "casual"
    generated_at = models.DateTimeField(auto_now_add=True)
    products = models.JSONField()  # Stores retail API product IDs