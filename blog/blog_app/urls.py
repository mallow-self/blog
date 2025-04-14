from django.urls import path
from .views import (
    BlogTableView,
    BlogAjaxDatatableView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    RegisterView,
    LoginView,
    LogoutView,
    initialize_groups,
)
from django.apps import apps

app_name: str = "blog"
urlpatterns: list = [
    #crud URLs
    path("", BlogTableView.as_view(), name="blog_list"),
    path("blogs_ajax/", BlogAjaxDatatableView.as_view(), name="blog_ajax"),
    path("blog/<int:pk>", BlogDetailView.as_view(), name="detail"),
    path("create/", BlogCreateView.as_view(), name="blog_create"),
    path("edit/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete"),

    # Authentication URLs
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

# initialize groups when the app is loaded this will ensure that the required groups exist
if not apps.is_installed("blog_app.apps.BlogAppConfig"):
    initialize_groups()
