from django.shortcuts import render

from .models import Quote


def home(request):
    q = request.GET.get('q')

    if q:
        quotes = Quote.objects.filter(content__search=q)  # this
    else:
        quotes = []

    return render(request, 'index.html', {'quotes': quotes})
