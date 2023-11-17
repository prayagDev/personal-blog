from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from blog_comment.models import Comment
from blog_comment.forms import CommentForm
from django.shortcuts import render
# Create your views here.

@login_required
def update_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_slug=comment.post.slug
    if comment.author == request.user:
        if request.method=="POST":
            form = CommentForm(request.POST, instance=comment)

            if form.is_valid():
                form.save()
                return redirect('post_detail', slug=post_slug)
        else:
            form=CommentForm(instance=comment)
        return render(request, 'blog_comment/update_comment.html', {'form': form})
    else:
        return HttpResponse("No such comment available")

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_slug=comment.post.slug
    if comment.author == request.user:
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    else:
        return HttpResponse("No such comment available")