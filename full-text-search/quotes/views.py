from django.shortcuts import render
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchRank,
    SearchQuery,
    SearchVector,
)

from .models import Quote


def home(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('content', 'author__name')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_headline = SearchHeadline('content', query, highlight_all=True)
        quotes = (
            Quote.objects.annotate(rank=rank)
            .annotate(headline=search_headline)
            .order_by('-rank')
            .filter(rank__gt=0)
        )
    else:
        quotes = []

    return render(request, 'index.html', {'quotes': quotes})
