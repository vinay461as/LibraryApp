from rest_framework import serializers
from library.models import Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class AuthorImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'image')
        read_only_fields = ('id',)
