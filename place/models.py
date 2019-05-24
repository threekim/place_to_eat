from django.db import models
from django.shortcuts import reverse
from django.db.models import Q
from django.contrib.auth.models import User


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


DESSERT = ['카페 / 디저트', '베이커리']
DESSERT_Q = Q(detail_category__icontains='카페 / 디저트') | Q(detail_category__icontains='베이커리')

SOOL = ['일반 주점', '치킨 / 호프 / 펍', '칵테일 / 와인', '전통 주점 / 포차', '이자카야 / 오뎅 / 꼬치']
SOOL_Q = Q(detail_category__icontains='일반 주점') | \
         Q(detail_category__icontains='칵테일 / 와인') | \
         Q(detail_category__icontains='치킨 / 호프 / 펍') | \
         Q(detail_category__icontains='전통 주점 / 포차') | Q(detail_category__icontains='이자카야 / 오뎅 / 꼬치')