from rest_framework import serializers
from .models import Author,Book

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'