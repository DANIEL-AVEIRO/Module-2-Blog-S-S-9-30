from django.contrib import admin
from app import models

admin.site.register(models.PostModel)
admin.site.register(models.CategoryModel)
