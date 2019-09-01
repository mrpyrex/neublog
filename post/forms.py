from django import forms
from .models import Post, Comment


class PostEmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'thumb',
            'category',
        ]


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'body',
        ]


class SearchForm(forms.Form):
    query = forms.CharField(max_length=None)
