from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'

class CommentModelForm(forms.ModelForm):
    
    class Meta:
        model   = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'