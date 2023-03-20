from django.db import models


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    create_update = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    quantity = models.FloatField()
