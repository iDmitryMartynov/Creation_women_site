from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from django.urls import reverse


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


data_db = [ {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
            {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
            {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True}, ]


def index(request):
    return render(request, 'women/index.html', {'title':'Главная страница',
                                                 'menu': menu,
                                                 'posts': data_db})


def about(request):
    return render(request, 'women/about.html', {'title':
                                                 'О сайте'})

def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")