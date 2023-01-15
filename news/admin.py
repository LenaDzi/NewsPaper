from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comments

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comments)

# регистрация моделей, что бы увидеть их в панели администрарора

