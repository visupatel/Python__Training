from rest_framework import serializers
from .models import Author,Book,BookImages
    
class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImages
        fields = ('id','book','image') 

class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many = True)

    class Meta:
        model = Book
        fields = ('id','name','author','published_date','images')

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = Author
        fields = ('id','name','country','books')