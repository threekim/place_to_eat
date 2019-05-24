from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)


class Area(models.Model):
    name = models.CharField(max_length=10)


class Place(models.Model):
    area = models.ManyToManyField(Area, related_name='places')
    name = models.CharField(max_length=30)
    url = models.URLField()
    image_url = models.URLField(null=True)
    address = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    detail_category = models.CharField(max_length=30, null=True)
    price = models.CharField(max_length=30, null=True)
    car = models.CharField(max_length=20, null=True)
    opening_hour = models.CharField(max_length=20, null=True)