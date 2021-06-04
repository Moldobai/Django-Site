from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from .forms import *
from .models import *


# Create your views here.


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


    # def add_page(request):
    #     if request.method == 'POST':
    #         form = AddPostForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             # print(form.cleaned_data)
    #             form.save()
    #             return redirect('home')
    #     else:
    #         form = AddPostForm()
    #     return render(request, 'women/add_page.html', {'form':form,'title':'Добавление статьи'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена </h1>')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class SearchWomen( DataMixin ,ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return  Women.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        c_def = self.get_user_context(title='Поиск')
        return dict(list(context.items()) + list(c_def.items()))