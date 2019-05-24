from django.shortcuts import render, redirect, get_object_or_404
from .models import Area, Place
from bs4 import BeautifulSoup
from django.db.models import Q
import random
import requests

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
        for count, place in enumerate(places):
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
            size = count
        return place_list[random.randint(0, size)]


def search_view(request):
    if request.method == 'GET':
        return render(request, 'place/search_view.html')

    context = dict()
    search_key = request.POST.get('search_key'.strip())
    area_filter = Area.objects.filter(name=search_key)

    if area_filter.exists():
        area_places = area_filter[0].places
        count = area_places.count()
        random_index = random.randint(0, count-1)
        random_place = area_places[random_index]
        return redirect(random_place)

    search_place_list(search_key)
    food_type = request.GET.getlist('food_type', 'title')
    bob_Q = Q(__icontains=search_key) if '밥' in food_type else Q()
    sool_Q = Q(author__username__icontains=search_key) if '술' in food_type else Q()
    desert_Q = Q(text__icontains=search_key) if '후식' in food_type else Q()

    random_place = None
    return redirect(random_place)

def detail_view(request, place_id):
    get_object_or_404(Place, pk=place_id)
    return render(request, 'place/detail_view.html', )










