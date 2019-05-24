from django.urls import path
from .views import search_view, detail_view

app_name = 'place'

urlpatterns = [
    path('search/', search_view, name='search'),
    path('detail/<int:place_id>/', detail_view, name='detail'),
]