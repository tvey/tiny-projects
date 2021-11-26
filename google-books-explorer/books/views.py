from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import Query
from .utils import call_books_api, get_client_ip


class IndexView(TemplateView):
    template_name = 'index.html'


def search(request):
    query = request.GET.get('q')
    page = request.GET.get('page', 0)

    if not query:
        return JsonResponse({'error': 'Query is required.'}, status=400)
    Query.objects.create(query=query, ip=get_client_ip(request))
    return JsonResponse(call_books_api(query, page=page), safe=False)
