from django import forms
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


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

    # Get authors (users in Author group)
    author = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Author"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )

    # Get editors (users in Editor group)
    editor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Editor"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )

    # Get publishers (users in Publisher group)
    publisher = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Publisher"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )

    class Meta:
        model = Blog
        fields = (
            "title",
            "content",
            "image",
            "category",
            "author",
            "editor",
            "publisher",
        )


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), required=True
    )
    user_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
        required=True,
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "user_group", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full name into first_name and last_name
        full_name_parts = self.cleaned_data["full_name"].split(" ", 1)
        user.first_name = full_name_parts[0]
        user.last_name = full_name_parts[1] if len(full_name_parts) > 1 else ""
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # Use email as username

        if commit:
            user.save()
            # Add user to the selected group
            user_group = self.cleaned_data.get("user_group")
            user.groups.add(user_group)

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        required=True,
    )
