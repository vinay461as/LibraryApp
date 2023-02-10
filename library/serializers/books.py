from rest_framework import serializers
from library.models import Books
from .author import AuthorSerializer


class BooksSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Books
        fields = '__all__'

