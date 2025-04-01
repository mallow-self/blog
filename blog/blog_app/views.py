from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from .models import Blog
from ajax_datatable.views import AjaxDatatableView
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
    

class BlogTableView(TemplateView):
    """
    A view for displaying the list of blog posts.

    Attributes:
        template_name (str): The path to the template used for rendering the blog list.
    """
    try:
        template_name: str = "blog_app/blog_list.html"
    except (Exception) as e:
        print(f"Exception occured:{e}")

class BlogAjaxDatatableView(AjaxDatatableView):
    """
    A view for handling AJAX-based DataTable rendering for Blog entries.

    Attributes:
        model (Model): The Django model associated with the DataTable (Blog).
        title (str): The title displayed in the DataTable.
        search_fields (list[str]): Fields that support search functionality.
        column_defs (list[object]): Configuration for table columns, including visibility and orderability.
    """
    try:
        model = Blog
        title: str = "Blogs"
        search_fields: list[str] = ["title", "content", "category"]
        column_defs: list[object] = [
            {"name": "id", "title": "id", "visible": True, "orderable": True},
            {"name": "title", "title": "Title", "orderable": True},
            {"name": "content", "title": "Content", "orderable": False},
            {"name": "category", "title": "Category", "orderable": True},
        ]
    except (Exception) as e:
        print(f"Exception occured:{e}")


class BlogDetailView(DetailView):
    """
    A view for displaying the details of a specific blog post.

    Attributes:
        model (Model): The Django model associated with this view (Blog).
        template_name (str): The template used to render the blog detail page.
        context_object_name (str): The name of the object passed to the template context.
        http_method_names (list[str]): Allowed HTTP methods for this view.
    """
    try:
        model = Blog
        template_name: str = "blog_app/detail_base.html"
        context_object_name: str = "detail_data"
        http_method_names: list[str] = ["get"]
    except (Exception) as e:
        print(f"Exception occured:{e}")


class BlogCreateView(CreateView):
    """
    A view for creating a new blog post with support for AJAX requests.

    Attributes:
        model (Model): The Django model associated with this view (Blog).
        fields (list[str]): The fields to be displayed in the form.
        template_name (str): The template used to render the form.
        success_url (str): The URL to redirect to after a successful submission.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests. If the request is AJAX, returns only the form.
        
        form_valid(form):
            Handles successful form submission. Returns JSON response for AJAX requests.
        
        form_invalid(form):
            Handles form submission with errors. Returns JSON response with form errors for AJAX requests.
    """
    try:
        model = Blog
        fields: list[str] = ['title', 'content', 'image', 'category']
        template_name: str = 'blog_app/blog_form_partial.html'
        success_url = reverse_lazy('blog:blog_list')
    except (Exception) as e:
        print(f"Exception occured:{e}")

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form = self.get_form()
                return render(request, self.template_name, {'form': form})
            return super().get(request, *args, **kwargs)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        # Handle AJAX form submission
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Blog created successfully!',
                    'id': self.object.pk,
                })
            return super().form_valid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'html': render_to_string(self.template_name, {'form': form}, request=self.request)
                })
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")


class BlogUpdateView(UpdateView):
    """
    A view for updating an existing blog post with support for AJAX requests.

    Attributes:
        model (Model): The Django model associated with this view (Blog).
        fields (list[str]): The fields to be displayed in the update form.
        template_name (str): The template used to render the update form.
        success_url (str): The URL to redirect to after a successful update.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests. If the request is AJAX, returns only the form along with existing data.

        form_valid(form):
            Handles successful form submission. If no new image is uploaded and an existing image is present, 
            it retains the current image. Returns JSON response for AJAX requests.

        form_invalid(form):
            Handles form submission with errors. Returns JSON response with form errors for AJAX requests.
    """
    try:
        model = Blog
        fields: list[str] = ['title', 'content', 'image', 'category']
        template_name: str = 'blog_app/blog_form_partial.html'
        success_url = reverse_lazy('blog:blog_list')
    except (Exception) as e:
        print(f"Exception occured:{e}")

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = self.get_object()
                form = self.get_form()
                context = {
                    'form': form,
                    'object': self.object,
                    # Check if object has an image
                    'has_image': bool(self.object.image)
                }
                if self.object.image:
                    context['image_url'] = self.object.image.url

                return render(request, self.template_name, context)
            return super().get(request, *args, **kwargs)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        # Handle AJAX form submission
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Check if image field is empty in the POST but the object already has an image
                if not self.request.FILES.get('image') and 'image-clear' not in self.request.POST:
                    # Keep the existing image
                    self.object = form.save(commit=False)
                    # Get the existing Blog object and its image
                    existing_blog = get_object_or_404(Blog, pk=self.object.pk)
                    self.object.image = existing_blog.image

                    self.object.save()
                    form.save_m2m()  # Save many-to-many relationships if any
                else:
                    self.object = form.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Blog updated successfully!',
                    'id': self.object.pk,
                })
            return super().form_valid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = self.get_object()  # Need to get the object for the template
                context = {
                    'form': form,
                    'object': self.object,
                    'has_image': bool(self.object.image)
                }
                if self.object.image:
                    context['image_url'] = self.object.image.url

                return JsonResponse({
                    'success': False,
                    'html': render_to_string(self.template_name, context, request=self.request)
                })
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")


class BlogDeleteView(DeleteView):
    """
    A view for deleting a blog post with AJAX support.

    Attributes:
        model (Model): The Django model associated with this view (Blog).

    Methods:
        post(request, *args, **kwargs):
            Handles AJAX-based deletion of a blog post. Returns a JSON response upon success.
    """
    try:
        model = Blog
    except (Exception) as e:
        print(f"Exception occured:{e}")

    def post(self, request, *args, **kwargs):
        try:
            blog = get_object_or_404(Blog, pk=kwargs['pk'])
            blog.delete()
            return JsonResponse({
                'success': True,
                'message': 'Blog deleted successfully!'
            })
        except (Exception) as e:
            print(f"Exception occured:{e}")
