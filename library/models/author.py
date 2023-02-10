import uuid
import os
from django.db import models


def recipe_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe', filename)


class Author(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.IntegerField()
    fb_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    class Meta:
        unique_together = [("name", "surname")]

    def __str__(self):
        return f'{self.name} {self.surname}'
