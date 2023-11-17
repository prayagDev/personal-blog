from django.urls import path
from blog_comment.views import delete_comment, update_comment
urlpatterns = [
    path('update/<int:comment_id>/', update_comment, name='update_comment'),
    path('delete/<int:comment_id>/', delete_comment, name='delete_comment'),
]
    