from rest_framework import status
from .models import Student,Subject
from .serializers import StudentSerializer,SubjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Student post
@api_view(['POST'])
def create_student(request):

    try:
        stud_name = request.data.get('name')
        sub = request.data.get('subject')
        if not stud_name or not sub:
            return Response({"status" : "Failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        
        subject = Subject.objects.get(id=sub)
        Student.objects.create(name = stud_name,subject = subject)
        return Response({"status" : "success","message" : "Student Created Successfully"},status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# subject post
@api_view(['POST'])
def create_subject(request):

    try:
        sub = request.data.get('sub_name')
        if not sub:
            return Response({"status" : "Failed", "message" : "Not created"},status = status.HTTP_400_BAD_REQUEST)
        Subject.objects.create(sub_name = sub)
        return Response({"status" : "success","message" : "Subject Created Successfully"},status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# Student data fetch
@api_view(['GET'])
def get_student_data(request):
    try:
        stud_id = request.data.get('id')
        try:
            if stud_id:
                stud_data = Student.objects.get(id = stud_id)
            else:
                stud_data = Student.objects.all()

            serializer = StudentSerializer(stud_data,many = True)
            return Response({"status" : "success","message" : "Fetch Student data","data" : serializer.data},status = status.HTTP_200_OK)
            
        except Student.DoesNotExist:
            return Response({"status": "Failed", "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# Subject data fetch
@api_view(['GET'])
def get_subject(request):
    try:
        sub_id = request.data.get('id')
        try:
            if sub_id:
                sub_data = Subject.objects.get(id = sub_id)
            else:
                sub_data = Subject.objects.all()

            serializer = SubjectSerializer(sub_data,many = True)
            return Response({"status" : "success","message" : "Fetch Subject data","data" : serializer.data},status = status.HTTP_200_OK)
            
        except Subject.DoesNotExist:
            return Response({"status": "Failed", "message": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# update student data
@api_view(['POST'])
def update_student(request):
    std_id = request.data.get('id')
    new_name = request.data.get('name')
    sub_id = request.data.get('subject')

    try:
        std_data = Student.objects.get(id = std_id)
        serializer = StudentSerializer(std_data,data=request.data)
        sub = Subject.objects.get(id = sub_id)

        if serializer.is_valid():
            std_data.name = new_name
            std_data.subject = sub
            std_data.save()
            return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
        else:
            return Response({"status":"Failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

    except Student.DoesNotExist:
        return Response({"status": "Failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)




# update subject data
@api_view(['POST'])
def update_subject(request):
    sub_id = request.data.get('id')
    new_name = request.data.get('sub_name')

    try:
        sub_data = Subject.objects.get(id = sub_id)
        serializer = SubjectSerializer(sub_data,data=request.data)

        if serializer.is_valid():
            sub_data.sub_name = new_name
            sub_data.save()
            return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)
        else:
            return Response({"status":"Failed","message":"Not Found"},status= status.HTTP_404_NOT_FOUND)

    except Student.DoesNotExist:
        return Response({"status": "Failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)





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




# Delete subject data
@api_view(['POST'])
def delete_subject(request):
    try:
        sub_id = request.data.get('id')
        sub_data = Subject.objects.get(id = sub_id)
        sub_data.delete()
        return Response({"status" : "success", "message":f"Subject ID : '{sub_id}' deleted successfully"},status=status.HTTP_200_OK)
    except Subject.DoesNotExist:
        return Response({"status":"Failed","message":"Not Found"},status=status.HTTP_404_NOT_FOUND)