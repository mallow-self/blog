from django.shortcuts import render
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.views.generic import ListView, TemplateView, DetailView, UpdateView
from .models import Blog
from ajax_datatable.views import AjaxDatatableView
from django.template.response import TemplateResponse

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



