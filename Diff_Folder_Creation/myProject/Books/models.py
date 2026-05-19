from django.db import models

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    published_date = models.DateField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')

class BookImages(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='book_images/',default='',null=True)