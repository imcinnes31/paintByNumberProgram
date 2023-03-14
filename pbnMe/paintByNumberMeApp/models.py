from django.db import models

# Create your models here.
class ColorPixel(models.Model):
    fileName = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    colorNumber = models.IntegerField()
    paintArea = models.IntegerField()
    coordinates = models.JSONField()
    coorNum = models.IntegerField(default=0)
    xCenter = models.IntegerField(default=0)
    yCenter = models.IntegerField(default=0)
    areaSize = models.IntegerField(default=0)