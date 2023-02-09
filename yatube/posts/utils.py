from django.core.paginator import Paginator

from yatube.settings import NUMBER_OF_POST


def paginator(object, request):
    paginator = Paginator(object, NUMBER_OF_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
