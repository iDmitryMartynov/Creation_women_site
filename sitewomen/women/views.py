from turtle import title
from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from .utils import DataMixin

from .forms import AddPostForm, UploadFileForm
from .models import Category, TagPost, UploadFiles, Women


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.all().select_related('cat')



def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                   {'title': 'О сайте',
                    'menu': menu,
                    'form': form})




class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'


    

class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    

def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')




class ShowPost(DataMixin,DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    return render(request, 'women/index.html', {'title':f'Рубрика: {category.name}',
                                                 'menu': menu,
                                                 'posts': posts,
                                                 'cat_selected': category.pk})


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)



def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WomenTag(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Тег: ' + self.tag.tag)
        
    

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

