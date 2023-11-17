from django.contrib import admin
from blog_comment.models import Comment
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['id', 'post_link', 'author_link', 'created_date', 'updated_date']

    def post_link(self, obj):
        post_url = reverse("admin:blog_post_post_change", args=[obj.post.id])
        return mark_safe(f'<a href="{post_url}">{obj.post}</a>')
    
    def author_link(self, obj):
        author_url = reverse("admin:auth_user_change", args=[obj.author.id])
        return mark_safe(f'<a href="{author_url}">{obj.author}</a>')
    
    post_link.short_description = 'Post'
    author_link.short_description = 'Author'
