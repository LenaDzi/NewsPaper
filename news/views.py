from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import *
from django.http import HttpResponseRedirect

class PostsList(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'
    paginate_by = 2  #  указазываем количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['time_now'] = datetime.utcnow()
        #context['next_post'] = None
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    # ordering = 'title'
    template_name = 'news/post_1.html'
    context_object_name = 'post'

#def create_post(request):
   # if request.method =='POST':
    #    form = PostForm(request.POST)
     #   if form.is_valid():
      #      form.save()
       #     return HttpResponseRedirect('/news/')

  #  form = PostForm
   # return render(request, 'post_edit.html', {'form': form})

# Добавляем новое представление для создания товаров.
class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType ='AR'
        return super().form_valid(form)

 #Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class SearchPost(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'
    paginate_by = 2  # количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



