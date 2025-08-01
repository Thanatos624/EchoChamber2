from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects, now including an image field.
    """
    class Meta:
        model = Post
        # Add 'image' to the list of fields.
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    """
    A form for submitting comments.
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        labels = {
            'text': '' # Hide the label for the text field
        }
