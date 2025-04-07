from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.
class Blog(models.Model):
    CATEGORY_CHOICES: list[tuple[str, str]] = [
        ("python", "Python"),
        ("django", "Django"),
        ("powerbi", "PowerBI"),
        ("scrapy", "Scrapy"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields for user roles
    author = models.ForeignKey(
        User, related_name="authored_blogs", on_delete=models.CASCADE
    )
    editor = models.ForeignKey(
        User, related_name="edited_blogs", on_delete=models.CASCADE
    )
    publisher = models.ForeignKey(
        User, related_name="published_blogs", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
