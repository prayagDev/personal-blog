from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog_api.views import CategoryViewSet, UserSignupView, UserLoginView, UserProfileView, ChangePasswordView, PasswordResetView, PasswordResetConfirmView, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    #registration
    path('user/register/', UserSignupView.as_view(), name="user_register"),
    #login
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    #profile
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    #change password
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
    #reset password
    path('user/reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('user/reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    #post comments list
    path('post-comments/<slug:post_slug>/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name="post-comments"),
    #post comments detail
    path('post-comments/<slug:post_slug>/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="post-comment-detail"),

]