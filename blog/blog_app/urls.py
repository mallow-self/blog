from django.urls import path
from .views import BlogTableView, BlogAjaxDatatableView, BlogDetailView, BlogCreateView, BlogUpdateView
from django.conf.urls.static import static
from django.conf import settings
# from .views import BlogListView

app_name: str = "blog"
urlpatterns: list = [
    # path('', BlogListView.as_view(), name="blogs"),
    path("", BlogTableView.as_view(), name="blog_list"),
    path("blogs_ajax/", BlogAjaxDatatableView.as_view(), name="blog_ajax"),
    path('blog/<int:pk>', BlogDetailView.as_view(), name="detail"),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
]
