from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post

class PostsList(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context

class PostDetail(DetailView):
    model = Post
    # ordering = 'title'
    template_name = 'news/post_1.html'
    context_object_name = 'post'






