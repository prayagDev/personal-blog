from django.contrib import admin
from blog_post.models import Post, Category
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'author_link', 'created_date', 'updated_date']

    def author_link(self, obj):
        author_url = reverse("admin:auth_user_change", args=[obj.author.id])
        return mark_safe(f'<a href="{author_url}">{obj.author}</a>')
    
    author_link.short_description = 'Author'

admin.site.register(Category)
