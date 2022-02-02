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


def search(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('content', 'author__name_en')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_headline = SearchHeadline('content', query, highlight_all=True)
        quotes = (
            Quote.objects.annotate(rank=rank)
            .annotate(headline=search_headline)
            .order_by('-rank')
            .filter(rank__gt=0)
        )
        result = list(quotes.values('headline', 'author__name_en'))
        return JsonResponse(result, safe=False)

    return JsonResponse([])
