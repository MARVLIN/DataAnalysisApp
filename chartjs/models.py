from django.db import models


class Iteration(models.Model):
    name = models.CharField(max_length=100)

class Data(models.Model):
    iteration = models.OneToOneField(Iteration, on_delete=models.CASCADE, related_name='data')
    dark = models.ImageField(upload_to='media/')
    decoded = models.ImageField(upload_to='media/')
    disparity = models.ImageField(upload_to='media/')
    edited = models.ImageField(upload_to='media/')
    light = models.ImageField(upload_to='media/')
    lookup = models.ImageField(upload_to='media/')
    mask = models.ImageField(upload_to='media/')
    mse = models.FloatField(max_length=3, default=0.0)
    ssim_score = models.FloatField(max_length=3, default=0.0)
    edited_quality = models.TextField(max_length=50)

class ImageMetrics(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
