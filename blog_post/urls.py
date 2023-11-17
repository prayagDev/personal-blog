from django.urls import path
from blog_post.views import home, post_detail, category_post, search_post, PostCreate, PostRead, PostDelete, PostUpdate

urlpatterns = [
    path('post/create/', PostCreate.as_view(), name='create_post'),
    path('post/list/', PostRead.as_view(), name='read_post'),
    path('post/delete/<slug:slug>/', PostDelete.as_view(), name='delete_post'),
    path('post/update/<slug:slug>/', PostUpdate.as_view(), name='update_post'),


    path('', home, name="home"),
    path('post/<slug:slug>/', post_detail, name="post_detail"),
    path('posts/search/', search_post, name="search_post"),
    path('posts/<str:name>/', category_post, name="category_post"),

    
]