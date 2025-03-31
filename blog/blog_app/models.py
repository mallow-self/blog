from django.db import models
# Create your models here.

# Add type hints for remaining fields
class Blog(models.Model):
    CATEGORY_CHOICES: list[tuple[str,str]] = [("python", "Python"), ("django", "Django"),
                        ("powerbi", "PowerBI"), ("scrapy", "Scrapy")]
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
