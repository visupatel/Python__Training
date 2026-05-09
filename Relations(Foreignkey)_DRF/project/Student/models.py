from django.db import models

# Subject model
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_name
    
# Student model
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='students')

    def __str__(self):
        return self.name
    

