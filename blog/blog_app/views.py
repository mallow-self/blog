from django.shortcuts import render,  get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    CreateView,
    FormView,
    View,
)
from .models import Blog
from ajax_datatable.views import AjaxDatatableView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .form import BlogForm, RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import review_mail, update_mail, delete_mail

class RegisterView(CreateView):
    template_name = "blog_app/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("blog:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! Please login.")
        return response


class LoginView(FormView):
    template_name = "blog_app/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.get_full_name()}!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid email or password.")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("blog:login")


def initialize_groups():
    """Create the three required groups if they don't exist."""
    group_names = ["Author", "Editor", "Publisher"]
    for group_name in group_names:
        Group.objects.get_or_create(name=group_name)


class BlogTableView(LoginRequiredMixin, TemplateView):
    """
    A view for displaying the list of blog posts.
    Requires user to be logged in.
    """

    try:
        template_name: str = "blog_app/blog_list.html"
        login_url = reverse_lazy("blog:login")
    except Exception as e:
        print(f"Exception occured:{e}")


class BlogAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """
    A view for handling AJAX-based DataTable rendering for Blog entries.
    Requires user to be logged in.
    """

    try:
        model = Blog
        title: str = "Blogs"
        search_fields: list[str] = [
            "title",
            "content",
            "category",
            "author__first_name",
            "author__last_name",
        ]
        column_defs: list[object] = [
            {"name": "id", "title": "id", "visible": True, "orderable": True},
            {"name": "title", "title": "Title", "orderable": True},
            {"name": "content", "title": "Content", "orderable": False},
            {"name": "category", "title": "Category", "orderable": True},
            {
                "name": "author",
                "title": "Author",
                "orderable": True,
                "foreign_field": "author__first_name",
                "placeholder": True,
                "choices": True,
                "autofilter": True,
            },
        ]
        login_url = reverse_lazy("blog:login")
    except Exception as e:
        print(f"Exception occured:{e}")


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    A view for displaying the details of a specific blog post.
    Requires user to be logged in.
    """

    try:
        model = Blog
        template_name: str = "blog_app/detail_base.html"
        context_object_name: str = "detail_data"
        http_method_names: list[str] = ["get"]
        login_url = reverse_lazy("blog:login")
    except Exception as e:
        print(f"Exception occured:{e}")


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    A view for creating a new blog post with support for AJAX requests.
    Requires user to be logged in and have proper permissions.
    """

    try:
        model = Blog
        form_class = BlogForm
        template_name: str = "blog_app/blog_form_partial.html"
        success_url = reverse_lazy("blog:blog_list")
        login_url = reverse_lazy("blog:login")
    except Exception as e:
        print(f"Exception occured:{e}")

    def test_func(self):
        """Check if user belongs to Author, Editor, or Publisher group"""
        return self.request.user.groups.filter(
            name__in=["Author", "Editor", "Publisher"]
        ).exists()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Set current user as default author if they are in the Author group
        if self.request.user.groups.filter(name="Author").exists():
            form.fields["author"].initial = self.request.user
        return form

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                form = self.get_form()
                return render(request, self.template_name, {"form": form})
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        # Handle AJAX form submission
        try:
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                self.object = form.save()

                # Send email to publisher and editor
                review_mail(self.object)

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Blog created successfully!",
                        "id": self.object.pk,
                    }
                )
            return super().form_valid(form)
        except Exception as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        try:
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": False,
                        "html": render_to_string(
                            self.template_name, {"form": form}, request=self.request
                        ),
                    }
                )
            return super().form_invalid(form)
        except Exception as e:
            print(f"Exception occured:{e}")


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for updating an existing blog post with support for AJAX requests.
    Requires user to be logged in and have proper permissions.
    """

    try:
        model = Blog
        form_class = BlogForm
        template_name: str = "blog_app/blog_form_partial.html"
        success_url = reverse_lazy("blog:blog_list")
        login_url = reverse_lazy("blog:login")
    except Exception as e:
        print(f"Exception occured:{e}")

    def test_func(self):
        """Check if user belongs to Editor or Publisher group"""
        return self.request.user.groups.filter(
            name__in=["Editor", "Publisher"]
        ).exists()

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                self.object = self.get_object()
                form = self.get_form()
                context = {
                    "form": form,
                    "object": self.object,
                    # Check if object has an image
                    "has_image": bool(self.object.image),
                }
                if self.object.image:
                    context["image_url"] = self.object.image.url

                return render(request, self.template_name, context)
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        # Handle AJAX form submission
        try:
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                # Check if image field is empty in the POST but the object already has an image
                if (
                    not self.request.FILES.get("image")
                    and "image-clear" not in self.request.POST
                ):
                    # Keep the existing image
                    self.object = form.save(commit=False)
                    # Get the existing Blog object and its image
                    existing_blog = get_object_or_404(Blog, pk=self.object.pk)
                    self.object.image = existing_blog.image

                    self.object.save()
                    form.save_m2m()  # Save many-to-many relationships if any
                    # Send mail to author,publisher
                    update_mail(self.object)
                else:
                    self.object = form.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Blog updated successfully!",
                        "id": self.object.pk,
                    }
                )
            return super().form_valid(form)
        except Exception as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        try:
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                self.object = (
                    self.get_object()
                )  # Need to get the object for the template
                context = {
                    "form": form,
                    "object": self.object,
                    "has_image": bool(self.object.image),
                }
                if self.object.image:
                    context["image_url"] = self.object.image.url

                return JsonResponse(
                    {
                        "success": False,
                        "html": render_to_string(
                            self.template_name, context, request=self.request
                        ),
                    }
                )
            return super().form_invalid(form)
        except Exception as e:
            print(f"Exception occured:{e}")


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    login_url = reverse_lazy("blog:login")

    def test_func(self):
        return self.request.user.groups.filter(name="Publisher").exists()

    def post(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(pk=kwargs["pk"])
            # send mail to author and editor
            delete_mail(blog)
            blog.delete()
            
            return JsonResponse(
                {"success": True, "message": "Blog deleted successfully!"}
            )
        except Blog.DoesNotExist:
            return JsonResponse({"success": False, "message": "Blog not found."})
        except Exception as e:
            print(f"Exception occurred: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "message": "An error occurred while deleting the blog.",
                }
            )
