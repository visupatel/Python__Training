from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField()

    def __str__(self):
        return self.name