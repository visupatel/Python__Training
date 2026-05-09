from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)


class Student_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_info')
    branch = models.CharField(max_length=20)
    dept = models.CharField(max_length=30)
    image = models.ImageField(upload_to='std_image',blank=True)


