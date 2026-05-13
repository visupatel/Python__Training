from rest_framework import status
from .models import Student,Subject
from .serializers import StudentSerializer,SubjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

# Student post
@api_view(['POST'])
def create_student(request):

    try:
        stud_name = request.data.get('name')
        sub = request.data.get('subject_id')

        if not stud_name or not sub:
            return Response({"status" : "failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        
        try:
            subject = Subject.objects.get(id = sub)
        except Subject.DoesNotExist:
            return Response({"status": "failed", "message": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            Student.objects.create(name = stud_name,subject = subject)
            return Response({"status" : "success","message" : "Student Created Successfully"},status= status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"status":"error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# subject post
@api_view(['POST'])
def create_subject(request):

    try:
        sub = request.data.get('sub_name')
        if not sub:
            return Response({"status" : "failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            Subject.objects.create(sub_name = sub)
            return Response({"status" : "success","message" : "Subject Created Successfully"},status= status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Student data fetch
@api_view(['POST'])
def get_student_data(request):
    try:
        stud_id = request.data.get('id')

        try:
            stud_data = Student.objects.all()
            if stud_id:
                stud_data = Student.objects.filter(id = stud_id)
        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(stud_data,many = True)
        return Response({"status" : "success","message" : "Fetch Student data","data" : serializer.data},status = status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"status":"error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Subject data fetch
@api_view(['POST'])
def get_subject(request):
    try:
        sub_id = request.data.get('id')
        try:
            sub_data = Subject.objects.all()
            if sub_id:
                sub_data = Subject.objects.filter(id = sub_id)
        except Subject.DoesNotExist:
            return Response({"status": "failed", "message": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubjectSerializer(sub_data,many = True)
        return Response({"status" : "success","message" : "Fetch Subject data","data" : serializer.data},status = status.HTTP_200_OK)
            
        
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# update student data
@api_view(['PUT'])
def update_student(request):

    try:
        std_id = request.data.get('id')
        new_name = request.data.get('name')
        sub_id = request.data.get('subject')

        try:

            if not std_id:
                return Response({"status":"failed", "message":"'id' must be required"},status=status.HTTP_400_BAD_REQUEST)

            std_data = Student.objects.get(id = std_id)
            serializer = StudentSerializer(std_data,data=request.data)
            if sub_id:
                sub = Subject.objects.get(id = sub_id)
                std_data.subject = sub
                std_data.save()

            if serializer.is_valid():

                if new_name:
                    std_data.name = new_name
    
                std_data.save()
                return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
            else:
                return Response({"status":"failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

        except Student.DoesNotExist:
            return Response({"status": "failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


# update subject data
@api_view(['PUT'])
def update_subject(request):
    sub_id = request.data.get('id')
    new_name = request.data.get('sub_name')

    try:
        if not sub_id:
            return Response({"status":"failed", "message":"'id' must be required"},status=status.HTTP_400_BAD_REQUEST)
        sub_data = Subject.objects.get(id = sub_id)
        serializer = SubjectSerializer(sub_data,data=request.data)

        if serializer.is_valid():
            sub_data.sub_name = new_name
            sub_data.save()
            return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
        else:
            return Response({"status":"failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

    except Student.DoesNotExist:
        return Response({"status": "failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)


# Delete student data
@api_view(['DELETE'])
def delete_student(request):
    try:
        std_id = request.data.get('id')
        try:
            std_data = Student.objects.get(id = std_id)
        except Student.DoesNotExist:
            return Response({"status":"failed","message":"Student Not Found"},status=status.HTTP_404_NOT_FOUND)

        std_data.delete()
        return Response({"status" : "success", "message":f"Student ID : '{std_id}' deleted successfully"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete subject data
@api_view(['DELETE'])
def delete_subject(request):
    try:
        sub_id = request.data.get('id')

        try:
            sub_data = Subject.objects.get(id = sub_id)
        except Subject.DoesNotExist:
            return Response({"status":"failed","message":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        sub_data.delete()
        return Response({"status" : "success", "message":f"Subject ID : '{sub_id}' deleted successfully"},status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
