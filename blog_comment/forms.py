from django import forms 
from blog_comment.models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Your Comment',
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'class':'form-control'
            }
        )
    )
    class Meta:
        model=Comment
        fields=['content']