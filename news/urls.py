from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPost, CategoryList, subscribe
from .views import ProtectedView
from .views import UserProfileUpdate
from .views import upgrade_user


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchPost.as_view(), name='search_post'),
    path('<int:pk>/profile/', UserProfileUpdate.as_view()),
    path('upgrade/', upgrade_user, name='upgrade'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe')
]