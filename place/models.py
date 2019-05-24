from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
import requests


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

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.detail_category in ('카페 / 디저트', '베이커리'):
            self.category = Category.objects.get(name='후식')

        elif self.detail_category in ('일반 주점', '치킨 / 호프 / 펍', '칵테일 / 와인', '전통 주점 / 포차', '이자카야 / 오뎅 / 꼬치'):
            self.category = Category.objects.get(name='술')

        else:
            self.category = Category.objects.get(name='밥')

        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_absolute_url(self):
        return reverse('place:detail', args=[self.id])

    def address_to_location(self):

        url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="+self.address+"&coordinate=11,10"
        custom_headers = {
            "X-NCP-APIGW-API-KEY-ID" : 'utkqk0r5dp',
            "X-NCP-APIGW-API-KEY" : "oc9RIxevNLeRbwhMECDKOqlt5EAdRPqi5BpdW4rE"
        }
        req=requests.get(url, headers=custom_headers)
        try:
            return (req.json()["addresses"][0]["x"], req.json()["addresses"][0]["y"])
        except:
            print(self.address, '좌표화 불가')
            return None