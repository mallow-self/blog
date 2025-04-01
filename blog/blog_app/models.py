from django.db import models
# Create your models here.


class Blog(models.Model):
    CATEGORY_CHOICES: list[tuple[str,str]] = [("python", "Python"), ("django", "Django"),
                        ("powerbi", "PowerBI"), ("scrapy", "Scrapy")]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)