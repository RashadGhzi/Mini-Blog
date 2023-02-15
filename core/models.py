from django.db import models

# Create your models here.


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    REQUIRED_FIELDS = ["title", "description"]
