from rest_framework import serializers
from .models import Student,Subject


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name')


class SubjectSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)
    class Meta:
        model = Subject
        fields = ('id','sub_name','students')




