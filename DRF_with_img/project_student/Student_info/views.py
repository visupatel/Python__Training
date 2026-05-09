from django.shortcuts import render
from rest_framework.response import Response
from .models import Student,Student_Profile
from rest_framework import status
from rest_framework.decorators import api_view


# post
@api_view(['POST'])
def create_student(request):
    std_id = request.data.get('id')
    std_name = request.data.get('name')
    std_mobile_no = request.data.get('mobile_no')

    try:
        if not std_id:
            return Response({"status" : "Failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        Student.objects.create(name = std_name,mobile_no = std_mobile_no)
        return Response({"status" : "success","message" : "Student Created Successfully"},status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# post
@api_view(['POST'])
def create_student_profile(request):
    profile_id = request.data.get('id')
    std_id = request.data.get('std_id')
    branch = request.data.get('branch')
    department = request.data.get('dept')
    img = request.data.get('image')

    try:
        if not std_id or not profile_id:
            return Response({"status" : "Failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        std = Student.objects.get(id = std_id)
        Student_Profile.objects.create(student = std,branch = branch,dept = department,image = img)
        return Response({"status" : "success","message" : "Student Profile Created Successfully"},status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# Get student
@api_view(['GET'])
def get_student(request):

    std_id = request.data.get('id')

    try:
        if std_id:
            std_data = Student.objects.filter(id = std_id)
        
        else:
            std_data = Student.objects.all()
        
        std_info = []
        for detail in std_data:
            temp = {"id":detail.id,"name":detail.name, "mobile_no":detail.mobile_no}
            std_info.append(temp)

        return Response({"status" : "success", "message" : "Fetch student data...", "student":std_info})
    except Student.DoesNotExist:
        return Response({"status": "Failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# Get student
@api_view(['GET'])
def get_student_profile(request):

    profile_id = request.data.get('id')

    try:
        if profile_id:
            std_profile = Student_Profile.objects.filter(id = profile_id)
        
        else:
            std_profile = Student_Profile.objects.all()
        
        std_data = []
        for detail in std_profile:
            temp = {"id":detail.id,"student" : detail.student.id,"branch":detail.branch, "dept":detail.dept,"image" : detail.image.url}
            std_data.append(temp)

        return Response({"status" : "success", "message" : "Fetch student Profile...", "student_profile":std_data})
    except Student_Profile.DoesNotExist:
        return Response({"status": "Failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    




# update student
@api_view(['POST'])
def update_student(request):
    std_id = request.data.get('id')
    new_name = request.data.get('name')
    new_mobile_no = request.data.get('mobile_no')

    try:

        if not std_id:
            return Response({"status":"Failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

        std_data = Student.objects.get(id = std_id)
        std_data.name = new_name
        std_data.mobile_no = new_mobile_no
        std_data.save()
        return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
            
    except Student.DoesNotExist:
        return Response({"status": "Failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# update student profile
@api_view(['POST'])
def update_student_profile(request):
    profile_id = request.data.get('id')
    std_id = request.data.get('std_id')
    branch = request.data.get('branch')
    department = request.data.get('dept')
    img = request.data.get('image')

    try:

        if not std_id or not profile_id:
            return Response({"status":"Failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

        std = Student.objects.get(id = std_id)
        std_profile = Student_Profile.objects.get(id = profile_id)
        std_profile.student = std
        std_profile.branch = branch
        std_profile.dept = department
        std_profile.image = img

        std_profile.save()
        return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
            
    except Student.DoesNotExist:
        return Response({"status": "Failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    




# Delete student data
@api_view(['POST'])
def delete_student(request):
    try:
        std_id = request.data.get('id')
        std_data = Student.objects.get(id = std_id)
        std_data.delete()
        return Response({"status" : "success", "message":f"Student ID : '{std_id}' deleted successfully"},status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({"status":"Failed","message":"Not Found"},status=status.HTTP_404_NOT_FOUND)
