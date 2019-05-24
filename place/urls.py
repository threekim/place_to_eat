from django.urls import path
from .views import search_view, detail_view, PlaceLike, PlaceFavorite

app_name = 'place'

urlpatterns = [
    path('detail/<int:place_id>/', detail_view, name='detail'),
    path('like/<int:place_id>/', PlaceLike.as_view(), name ='like'),
    path('favorite/<int:place_id>/', PlaceFavorite.as_view(), name='favorite'),
    path('', search_view, name='search'),
]