from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Category, TagPost, UploadFiles, Women


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]



# def index(request):
#     posts = Women.published.all().select_related('cat')
#     return render(request, 'women/index.html', {'title':'Главная страница',
#                                                  'menu': menu,
#                                                  'posts': posts,
#                                                  'cat_selected': 0})


class WomenHome(ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title':'Главная страница',
        'menu': menu,
        'cat_selected': 0
    }

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.all().select_related('cat')


    # template_name = 'women/index.html'
    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

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

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)


class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи'
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class UpdatePage(UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи'
    }


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()

#         data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form
#                 }
#         return render(request, 'women/addpage.html', data)


#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
        
#         data = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form
#                 }
#         return render(request, 'women/addpage.html', data)

def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     data = {'title':post.title,
#             'menu': menu,
#             'post': post,
#             'cat_selected': 1}
#     return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    return render(request, 'women/index.html', {'title':f'Рубрика: {category.name}',
                                                 'menu': menu,
                                                 'posts': posts,
                                                 'cat_selected': category.pk})


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WomenTag(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тег: ' + self.tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context
    

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

