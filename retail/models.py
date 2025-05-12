from django.db import models

# Create your models here.
class RetailProduct(models.Model):
    api_id = models.CharField(max_length=100)  # ID from Shopify/Amazon
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()