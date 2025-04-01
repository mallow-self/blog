from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Enter title...'}),
        label="Title",
        required=True
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter content...'}),
        label="Content",
        required=True
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        ),
        label="Image",
        required=True
    )
    category = forms.ChoiceField(
        choices=Blog.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Category",
        required=True
    )
    class Meta:
        model = Blog
        fields = ("title", "content", "image", "category")