from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from .models import Area, Place, BOB_Q, SOOL_Q, DESSERT_Q
from bs4 import BeautifulSoup
from django.db.models import Q
import random
import requests
from django.views.generic.base import View
from django.http import HttpResponseForbidden, HttpResponseRedirect
from urllib.parse import urlparse
from django.views.generic.list import ListView
from django.contrib import messages


CUSTOM_HEADER = {
    'referer': 'https://www.naver.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def search_place_list(search_key):

    for i in range(1, 5):
        page_url = "https://www.mangoplate.com/search/?keyword="+str(search_key)+"&page="+str(i)
        page_request = requests.get(page_url, headers=CUSTOM_HEADER)
        soup = BeautifulSoup(page_request.text, "html.parser")
        places = soup.select("figure.restaurant-item ")
        place_list = list()
        count = 0
        for place in places:
            place_img_url = place.select_one("img").get('data-original')
            if place_img_url is None:
                continue

            place_url = "https://www.mangoplate.com" + place.select_one(".info a").get('href')
            place_request = requests.get(place_url, headers=CUSTOM_HEADER)
            place_soup = BeautifulSoup(place_request.text, "html.parser")
            place_name = place_soup.select_one('h1.restaurant_name').text
            place_info = place_soup.select('table.info tr')

            place_dict = dict()
            for tr in place_info:
                place_dict[tr.select_one('th').text.replace('\n', '').strip()] = tr.select_one('td').text.replace('\n', '')

            place_address = place_dict.get('주소')
            place_phone = place_dict.get('전화번호')
            place_detail_category = place_dict.get('음식 종류')
            place_price = place_dict.get('가격대')
            if place_price is None:
                continue
            place_car = place_dict.get('주차')
            place_opening_hour = place_dict.get('영업시간')

            place_obj = Place(name=place_name,
                              url=place_url,
                              image_url=place_img_url,
                              address=place_address,
                              phone=place_phone,
                              detail_category=place_detail_category,
                              price=place_price,
                              car=place_car,
                              opening_hour=place_opening_hour)
            place_obj.save()
            place_list.append(place_obj)
            count += 1
        return place_list[random.randint(0, count)]


def search_view(request):
    if request.method == 'GET':
        return render(request, 'place/search_view.html')

    food_type = request.POST.getlist('food_type', '밥')
    bob_Q = Q(category_Category_id=3) if '밥' in food_type else Q()
    sool_Q = Q(category_Category_id=1) if '술' in food_type else Q()
    desert_Q = Q(category_Category_id=2) if '후식' in food_type else Q()

    money_type = request.POST.getlist('money_type', '만원')
    money1_Q = Q(price='만원 미만') if '만원' in money_type else Q()
    money2_Q = Q(price='만원-2만원') if '2만원' in money_type else Q()
    money3_Q = Q(price='2만원-3만원') if '2만원이상' in money_type else Q()
    search_key = request.POST.get('search_key'.strip())

    area_filter = Area.objects.filter(name=search_key)

    if area_filter.exists():
        area_places = area_filter[0].places.filter(bob_Q| sool_Q| desert_Q| money1_Q| money2_Q| money3_Q)
        count = area_places.count()
        random_index = random.randint(0, count-1)
        random_place = area_places[random_index]
        return redirect(random_place)

    search_place_list(search_key)
    place_filter = Place.objects.filter(bob_Q| sool_Q| desert_Q| money1_Q| money2_Q| money3_Q)
    place_count = place_filter.count()
    random_index = random.randint(0, place_count-1)
    random_place = place_filter[random_index]
    return redirect(random_place)


class Detail_view(DetailView):
    model = Place
    template_name_suffix = '_detail'


class PlaceLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'place_id' in kwargs:
                place_id = kwargs['place_id']
                place = Place.objects.get(pk=place_id)
                user = request.user
                if user in place.like.all():
                    place.like.remove(user)
                else:
                    place.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PlaceFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'place_id' in kwargs:
                place_id = kwargs['place_id']
                place = Place.objects.get(pk=place_id)
                user = request.user
                if user in place.favorite.all():
                    place.favorite.remove(user)
                else:
                    place.favorite.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PlaceLikeList(ListView):
    model = Place
    template_name = 'place/place_likelist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PlaceLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PlaceFavoriteList(ListView):
    model = Place
    template_name = 'place/place_favoritelist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PlaceFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset








