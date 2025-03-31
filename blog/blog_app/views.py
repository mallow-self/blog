from django.shortcuts import render
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView
from .models import Blog
from ajax_datatable.views import AjaxDatatableView
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string


# Create your views here.
# class BlogListView(ListView):
#     model = Blog
#     template_name = "blog_app/blog_list.html"
#     context_object_name = "blog_data"
#     http_method_names = ["get"]
#     view_is_async = True

#     async def get(self, request, *args, **kwargs):
#         """Function to make the view async"""
        
#         # blog_queryset = await sync_to_async(list)(Blog.objects.all())
#         # if request.headers.get("X-Requested-With") == "XMLHttpRequest":
#         #     return JsonResponse({"blogs": [blog.to_dict() for blog in blog_queryset]})
#         return super().get(request, *args, **kwargs)  # Default template rendering
    

class BlogTableView(TemplateView):
    template_name = "blog_app/blog_list2.html"


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
    template_name = 'blog_app/blog_form_partial.html'
    success_url = reverse_lazy('blog:blog_list')
    fields = ["title","content","image","category"]

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
    template_name = 'blog_app/blog_form_partial.html'
    success_url = reverse_lazy('blog:blog_list')
    fields = ["title", "content", "image", "category"]

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object = self.get_object()
            form = self.get_form()
            return render(request, self.template_name, {'form': form, 'object': self.object})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Handle AJAX form submission
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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
            return JsonResponse({
                'success': False,
                'html': render_to_string(self.template_name, {'form': form, 'object': self.get_object()}, request=self.request)
            })
        return super().form_invalid(form)
