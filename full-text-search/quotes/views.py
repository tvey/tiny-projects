from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchRank,
    SearchQuery,
    SearchVector,
)

from .models import Quote


class IndexView(TemplateView):
    template_name = 'index.html'


class QuotesEn(TemplateView):
    template_name = 'quotes_en.html'


class QuotesRu(TemplateView):
    template_name = 'quotes_ru.html'


def search_util(lang):
    if lang == 'en':
        pass
    elif lang == 'ru':
        pass


def search(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('content')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_headline = SearchHeadline('content', query, highlight_all=True)
        quotes = (
            Quote.objects.annotate(rank=rank)
            .annotate(headline=search_headline)
            .order_by('-rank')
            .filter(rank__gt=0)
        )
        print(quotes)
        result = quotes.values('headline', 'author__name_en', 'author__name_ru')
        # print(list(result))
        return JsonResponse(list(result), safe=False)

    return JsonResponse([])
