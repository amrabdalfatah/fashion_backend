from django.db import models

# Create your models here.
class AnalysisResult(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    skin_tone = models.CharField(max_length=50)  # e.g., "Light", "Medium", "Dark"
    recommended_color = models.CharField(max_length=50)  # e.g., "Red", "Blue"
    confidence = models.FloatField()
    color_options = models.JSONField()  # List of color options
    created_at = models.DateTimeField(auto_now_add=True)
    
class OutfitRecommendation(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    occasion = models.CharField(max_length=100)  # e.g., "wedding", "casual"
    generated_at = models.DateTimeField(auto_now_add=True)
    products = models.JSONField()  # Stores retail API product IDs


# stylist_analysisresult
# stylist_outfitrecommendation