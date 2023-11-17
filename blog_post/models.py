from django.db import models
from django.contrib.auth.models import User  
from django.utils.text import slugify
import time, random, string 

class Category(models.Model):
    name=models.CharField(max_length=30, primary_key=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, default="Uncategorized")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str(int(time.time())) + ''.join(random.choices(string.ascii_letters, k=3))
            self.slug = f"{base_slug}-{unique_id}"
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
