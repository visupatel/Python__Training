from django.shortcuts import render
from rest_framework import status
from .models import Student
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .serializers import StudentSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage


# create student
@api_view(['POST'])
def create_student(request):

    try:
        std_name = request.data.get('name')
        std_roll = request.data.get('roll_no')
        
        with transaction.atomic():
            Student.objects.create(name = std_name, roll_no = std_roll)
            return Response({"status":"success","message":"student data created successfully..."},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
def get_student(request):

    try:
        std_id = request.data.get('id')
        search = request.data.get('search')
        page_number = request.data.get('page_number')
        page_size = request.data.get('page_size')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if not page_number or not page_size:
            return Response({"status":"failed","message":"page_number or page_size must be given"},status=status.HTTP_400_BAD_REQUEST)

        try:
            page_number = int(page_number)
            page_size = int(page_size)
        except ValueError:
            return Response({"status" : "failed", "message" : "Page_number and page_size must be integer"},status=status.HTTP_400_BAD_REQUEST)
        
        if page_number <= 0 or page_size <= 0:
            return Response({"status":"failed" ,"message":"page and page_size must be greater than 0"},status=status.HTTP_400_BAD_REQUEST)

        
        try:
            queryset = Student.objects.all()
        except Student.DoesNotExist:
            return Response({"status":"failed", "message":"Student not found"},status=status.HTTP_404_NOT_FOUND)
        
        if std_id :
            queryset = queryset.filter(id = std_id)

        if search:
            queryset = queryset.filter(Q(name__icontains = search) | Q(roll_no__icontains = search) )

        if start_date and end_date:
            queryset = queryset.filter(date__date__range = (start_date,end_date))

        paginator = Paginator(queryset,page_size)

        try:
            paginator_data = paginator.page(page_number)
        except EmptyPage:
            return Response({"status":"failed" ,"message": "Page number out of range"},status=status.HTTP_501_NOT_IMPLEMENTED)

        list_std = []
        for std in paginator_data:
            list_std.append({
                'id':std.id, 
                'name':std.name,
                'roll_no':std.roll_no,
                "date" : std.date.strftime("%Y-%m-%d %H:%M:%S") if std.date else None
            })

        return Response({
            "status":"success",
            "message":"Fetch student data...",
            "total_pages": paginator.num_pages,
            "current_page": page_number,
            "total_items": paginator.count,
            "students":list_std
            },
            status=status.HTTP_200_OK
            )
    
    except Exception as e:
        return Response({'status':'Error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# with serializer
@api_view(['POST'])
def get_std(request):

    try:
        std_id = request.data.get('id')
        search = request.data.get('search')
        page = request.data.get('page_number')
        page_size = request.data.get('page_size')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if not page or not page_size:
            return Response({"status":"Failed","message":"page or page_size must be given"},status=status.HTTP_400_BAD_REQUEST)
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return Response({"status":"failed" ,"message":"page and page_size must be integers"},status=status.HTTP_400_BAD_REQUEST)

        if page <= 0 or page_size <= 0:
            return Response({"status":"failed" ,"message":"page and page_size must be greater than 0"},status=status.HTTP_400_BAD_REQUEST)

        try:
            queryset = Student.objects.all()
        except Student.DoesNotExist:
            return Response({"status":"failed", "message":"Student not found"},status=status.HTTP_404_NOT_FOUND)
        
        if std_id :
            queryset = queryset.filter(id = std_id)

        if start_date and end_date:
            queryset = Student.objects.filter(date__date__range = (start_date,end_date))

        if search:
            queryset = queryset.filter(Q(name__icontains = search) | Q(roll_no__icontains = search))
        paginator = Paginator(queryset,page_size)

        try:
            paginated_data = paginator.page(page)
        except EmptyPage:
            return Response({"status":"failed" ,"message": "Page number out of range"},status=status.HTTP_400_BAD_REQUEST)

        serilizer = StudentSerializer(paginated_data,many = True)
        return Response({
            "status":"success",
            "message":"Fetch student data...",
            "total_pages": paginator.num_pages,
            "current_page": page,
            "total_items": paginator.count,
            "students":serilizer.data
            },
            status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'status':'Error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

