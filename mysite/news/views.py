from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    context = {"form": form}
    return render(request, 'news/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             'tchekalov.ruslan@yandex.ru',
                             ['tchekalov.ruslan@gmail.com'],
                             fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки!')
    else:
        form = ContactForm()
    context = {"form": form}
    return render(request, 'news/test.html', context)


class HomeNews(ListView, MyMixin):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'title': 'Главная страница'}
    mixin_prop = 'Hello world'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context = self.kwargs
        context['title'] = 'Главная страница'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')

# def index(request):
#     news = News.objects.all()
#     return render(request, 'news/index.html', {'news': news,
#                                                'title': 'Список новостей',
#                                                })
def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news,
                                               'category': category
                                               })

#def view_news(request, news_id):
#    #news_item = News.objects.get(pk=news_id)
#    news_item = get_object_or_404(News, pk=news_id)
#    return render(request, 'news/view_news.html', {"news_item": news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)    #Забираем из формы данные
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #News.objects.create(**form.cleaned_data)  # Операция распаковки словаря в Python
#             #return redirect('home')
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
