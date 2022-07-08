from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import TestMixin


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup is successful!')
            return redirect('home')
        else:
            messages.error(request, 'Signup error')
    else:
        form = UserRegisterForm()
    return render(request, 'news/signup.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/signin.html', {"form": form})


def signout(request):
    logout(request)
    return redirect('signin')


def contact(request):
    pass


def test(request):
    obj = ['andy', 'john', 'mike', 'philipp', 'joe', 'bob', 'michael']
    paginator = Paginator(obj, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    return render(request, 'news/test.html', {"page_obj": page_objects})


class BaseNews(TestMixin, ListView):
    model = News
    context_object_name = 'news'
    mixin_prop = 'Hello, World!'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['mixin_prop'] = self.get_prop()

        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(TestMixin, ListView):
    model = Category
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))

        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html '

# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#
#     return render(request, 'news/index.html', context)
#
#
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#
#     context = {
#         'news': news,
#         'category': category,
#     }
#
#     return render(request, 'news/category.html', context)


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/news_list.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#
#     return render(request, 'news/add_news.html', {'form': form})
