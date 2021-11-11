from django.http import JsonResponse
from django.views.generic import TemplateView

from .utils import call_books_api


class IndexView(TemplateView):
    template_name = 'index.html'


def search(request):
    query = request.GET.get('q')
    page = request.GET.get('page', 0)

    if not query:
        return JsonResponse({'error': 'Query is required.'}, status=400)
    return JsonResponse(call_books_api(query, page=page), safe=False)
