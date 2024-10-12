from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Category, TagPost, Women


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]



def index(request):
    posts = Women.published.all().select_related('cat')
    return render(request, 'women/index.html', {'title':'Главная страница',
                                                 'menu': menu,
                                                 'posts': posts,
                                                 'cat_selected': 0})


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте',
                                                'menu': menu})

def addpage(request):
    return render(request, 'women/addpage.html', {'title': 'Добавление статьи',
                                                'menu': menu})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {'title':post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 1}
    return render(request, 'women/post.html', data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    return render(request, 'women/index.html', {'title':f'Рубрика: {category.name}',
                                                 'menu': menu,
                                                 'posts': posts,
                                                 'cat_selected': category.pk})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)