from django.db import models

# Create your models here.
class Count(models.Model):
      areaName=models.CharField(max_length=10)
      avg_price=models.IntegerField()
      total=models.IntegerField()
      