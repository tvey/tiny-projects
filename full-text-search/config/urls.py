from django.contrib import admin
from django.urls import path

from quotes.views import IndexView, search, QuotesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('en/', QuotesView.as_view(), name='quotes-en'),
    path('ru/', QuotesView.as_view(), name='quotes-ru'),
    path('en/search/', search, name='search-en'),
    path('ru/search/', search, name='search-ru'),
]
