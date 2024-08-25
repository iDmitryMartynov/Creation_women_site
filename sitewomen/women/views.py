from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse


def index(request):
    return HttpResponse('Страница приложения women')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Страница по категориям</h1><p>id: {cat_id} </p>') 


def categories_by_slug(request, cat_slug):
    return HttpResponse(f'<h1>Страница по категориям</h1><p>slug: {cat_slug} </p>') 


def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('music',))
        return redirect(uri)
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year} </p>') 


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")