from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Страница')

def categories(request):
    return HttpResponse('<h1>Страница по категориям</h1>')
