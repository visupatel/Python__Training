from django.shortcuts import render
from rest_framework.response import Response
from .models import Student,Student_Profile
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import transaction


# post
@api_view(['POST'])
def create_student(request):
    std_name = request.data.get('name')
    std_mobile_no = request.data.get('mobile_no')

    try:
        with transaction.atomic():
            Student.objects.create(name = std_name,mobile_no = std_mobile_no)
            return Response({"status" : "success","message" : "Student Created Successfully"},status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# post
@api_view(['POST'])
def create_student_profile(request):
    std_id = request.data.get('std_id')
    branch = request.data.get('branch')
    department = request.data.get('dept')
    img = request.data.get('image')

    try:
        if not std_id :
            return Response({"status" : "failed", "message" : "'id' not found"},status = status.HTTP_404_NOT_FOUND)
        try: 
            std = Student.objects.get(id = std_id)
        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            Student_Profile.objects.create(student = std,branch = branch,dept = department,image = img)
            return Response({"status" : "success","message" : "Student Profile Created Successfully"},status= status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Get student
@api_view(['POST'])
def get_student(request):

    try:
        std_id = request.data.get('id')

        try:
            std_data = Student.objects.all()
            if std_id:
                std_data = Student.objects.filter(id = std_id)
        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        std_info = []
        for detail in std_data:
            std_info.append({
                "id":detail.id,
                "name":detail.name, 
                "mobile_no":detail.mobile_no
                })

        return Response({"status" : "success", "message" : "Fetch student data...", "student":std_info})
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Get student
@api_view(['POST'])
def get_student_profile(request):

    try:
        profile_id = request.data.get('id')
        try:
            std_profile = Student_Profile.objects.all()
            if profile_id:
                std_profile = Student_Profile.objects.filter(id = profile_id)
        except Student_Profile.DoesNotExist:
            return Response({"status": "failed", "message": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        std_data = []
        for detail in std_profile:
            std_data.append({
                "id":detail.id,
                "student" : detail.student.id,
                "branch":detail.branch, 
                "dept":detail.dept,
                "image" : detail.image.url,
                })

        return Response({"status" : "success", "message" : "Fetch student Profile...", "student_profile":std_data})
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# update student
@api_view(['PUT'])
def update_student(request):
    std_id = request.data.get('id')
    new_name = request.data.get('name')
    new_mobile_no = request.data.get('mobile_no')

    try:
        if not std_id:
            return Response({"status":"failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

        try:
            std_data = Student.objects.get(id = std_id)
        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)

        if new_name:
            std_data.name = new_name
        if new_mobile_no:
            std_data.mobile_no = new_mobile_no
        std_data.save()
        return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# update student profile
@api_view(['PUT'])
def update_student_profile(request):

    try:
        profile_id = request.data.get('id')
        std_id = request.data.get('std_id')
        branch = request.data.get('branch')
        department = request.data.get('dept')
        img = request.data.get('image')

        if not profile_id:
            return Response({"status":"failed","message":"Profile id not Found"},status= status.HTTP_404_NOT_FOUND)

        try:
            std_profile = Student_Profile.objects.get(id = profile_id)
        except Student_Profile.DoesNotExist:
            return Response({"status": "failed", "message": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            if std_id:
                std = Student.objects.get(id = std_id)
                std_profile.student = std
                std_profile.save()
        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if branch:
            std_profile.branch = branch

        if department:
            std_profile.dept = department

        if img:
            std_profile.image = img
        std_profile.save()
        return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Delete student data
@api_view(['DELETE'])
def delete_student(request):
    try:
        std_id = request.data.get('id')
        try:
            std_data = Student.objects.get(id = std_id)
        except Student.DoesNotExist:
            return Response({"status":"failed","message":"'id' Not Found"},status=status.HTTP_404_NOT_FOUND)

        std_data.delete()
        return Response({"status" : "success", "message":f"Student ID : '{std_id}' deleted successfully"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    