from django import forms 
from blog_post.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title', 'category', 'content']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }