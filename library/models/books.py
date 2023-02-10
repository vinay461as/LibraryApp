from django.db import models
# from django.conf import settings
from .author import Author


class Books(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ManyToManyField(Author, )
    book_pages = models.PositiveIntegerField()
    genre = models.PositiveIntegerField()
    release_date = models.DateField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
