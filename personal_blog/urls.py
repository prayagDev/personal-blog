from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog_post.urls')),
    path('comment/', include('blog_comment.urls')),
    path('accounts/', include('blog_auth.urls')),
    path('blog_api/', include('blog_api.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)