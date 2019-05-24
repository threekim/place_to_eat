from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('place.urls')),
    path('accounts/', include('accounts.urls')),
]
