from django.db import models

# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to="posts/")
    viewer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
