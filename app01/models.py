from django.db import models

# Create your models here.
class IpModel(models.Model):
    ip = models.CharField(max_length=64)
    score = models.IntegerField(default=50)
