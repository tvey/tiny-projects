from django.contrib import admin
from django.urls import path

from quotes.views import IndexView, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('search/', search, name='search'),
]
