from django.urls import path
from .views import search_view, detail_view, PlaceLike, PlaceFavorite, PlaceFavoriteList, PlaceLikeList

app_name = 'place'

urlpatterns = [
    path('detail/<int:place_id>/', detail_view, name='detail'),
    path('like/<int:place_id>/', PlaceLike.as_view(), name ='like'),
    path('favorite/<int:place_id>/', PlaceFavorite.as_view(), name='favorite'),
    path("like/", PlaceLikeList.as_view(), name="like_list"),
    path("favorite/", PlaceFavoriteList.as_view(), name="favorite_list"),
    path('', search_view, name='search'),
]