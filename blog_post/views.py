from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect
from blog_post.models import Post, Category
from blog_post.forms import PostForm
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from blog_comment.forms import CommentForm
# Create your views here.

def home(request):
    category=Category.objects.all()
    recent_posts=Post.objects.all().order_by("-created_date")
    paginator = Paginator(recent_posts, 2)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        recent_posts = paginator.page(page)
    except PageNotAnInteger:
        recent_posts = paginator.page(1)
    except EmptyPage:
        recent_posts = paginator.page(paginator.num_pages)
    context={'recent_posts':recent_posts, 'category':category}
    return render(request, "blog_post\home.html", context)

def post_detail(request, slug):
    my_post=Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = my_post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    context={'my_post':my_post, 'form':form}
    return render(request, "blog_post\post_detail.html", context)

def category_post(request, name):
    category=Category.objects.get(name=name)
    c_post=Post.objects.filter(category__icontains=category).order_by("-created_date")
    context={'c_post':c_post}
    return render(request, "blog_post\category_post.html", context)

def search_post(request):
    keyword=request.GET.get('search')
    posts=Post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(category__icontains=keyword))
    context={'posts':posts, 'keyword':keyword}
    return render(request, "blog_post\search_post.html", context)

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class=PostForm
    template_name = 'blog_post/post_create.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('read_post')
    
class PostRead(LoginRequiredMixin, ListView):
    model = Post 
    template_name = 'blog_post/post_read.html' 
    context_object_name = 'object_list'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog_post/post_delete.html'
    success_url = reverse_lazy('read_post')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog_post/post_create.html'
    form_class = PostForm  
    success_url = reverse_lazy('read_post') 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)