from django.urls import path
from . import views
from typing import List

app_name: str = "blog"
urlpatterns: List = [
    path('', views.index, name="index"),
]
