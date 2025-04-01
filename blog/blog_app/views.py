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
    template_name = "blog_app/blog_list.html"


class BlogAjaxDatatableView(AjaxDatatableView):
    model = Blog
    title = "Blogs"
    search_fields = ["title", "content", "category"]
    column_defs = [
        {"name": "id", "title": "id", "visible": True, "orderable": True},
        {"name": "title", "title": "Title", "orderable": True},
        {"name": "content", "title": "Content", "orderable": False},
        {"name": "category", "title": "Category", "orderable": True},
    ]


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog_app/detail_base.html"
    context_object_name = "detail_data"
    http_method_names = ["get"]


# update and create

class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image', 'category']
    template_name = 'blog_app/blog_form_partial.html'
    success_url = reverse_lazy('blog:blog_list')

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = self.get_form()
            return render(request, self.template_name, {'form': form})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Handle AJAX form submission
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Blog created successfully!',
                'id': self.object.pk,
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'html': render_to_string(self.template_name, {'form': form}, request=self.request)
            })
        return super().form_invalid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'category']
    template_name = 'blog_app/blog_form_partial.html'
    success_url = reverse_lazy('blog:blog_list')

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
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

    def form_valid(self, form):
        # Handle AJAX form submission
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

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
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


class BlogDeleteView(DeleteView):
    model = Blog

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        blog.delete()
        return JsonResponse({
            'success': True,
            'message': 'Blog deleted successfully!'
        })
    
    # success_url = reverse_lazy('blog:blog_list')
