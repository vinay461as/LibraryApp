from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from serializers import BooksSerializer
from library.models import Books


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('title', 'author__name', 'book_pages', 'release_date')
