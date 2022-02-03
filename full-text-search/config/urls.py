from django.contrib import admin
from django.urls import path

from quotes.views import IndexView, search, QuotesEn, QuotesRu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('en/', QuotesEn.as_view(), name='quotes-en'),
    path('ru/', QuotesRu.as_view(), name='quotes-ru'),
    path('en/search/', search, name='search'),
    path('ru/search/', search, name='search'),
]
