from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=100)
    published_date = models.DateField()

class BookImages(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to = 'images',blank=True,null = True, default='')

class Author(models.Model):
    name = models.CharField(max_length=50)
    books = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='authors')
    country = models.CharField()

