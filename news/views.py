from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin


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
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    ordering = 'title'
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
class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType ='AR'
        return super().form_valid(form)

 #Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)

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


class UserProfileUpdate(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile.html'
class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    common_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name='common').exists():
        common_group.user_set.add(user)
    return redirect('/')

@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.create(authorUser=User.objects.get(pk=user.id))
    return redirect('/')

class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):  # фильтрация по категории
        # выдаст ошибку 404, если категории не существует
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('dataCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribe'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context

#подписка на категорию
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    massage = "Вы успешно подписались на рассылку"

    return render(request, 'news/subscribe.html', {'category': Category, 'massage': massage})


