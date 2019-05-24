from django.urls import path
from .views import search_view, Detail_view, PlaceLike, PlaceFavorite

app_name = 'place'

urlpatterns = [
    path('search/', search_view, name='search'),
    path('detail/<int:place_id>/', Detail_view, name='detail'),
    path('like/<int:place_id>/', PlaceLike.as_view(), name ='like'),
    path('favorite/<int:place_id>/', PlaceFavorite.as_view(), name='favorite'),
]