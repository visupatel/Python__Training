from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book,Author,BookImages
from .serializers import BookSerializer,AuthorSerializer
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from datetime import date


# create book
@api_view(['POST'])
def create_book(request):

    try:
        book_name = request.data.get('name')
        published_date = request.data.get('date')
        
        with transaction.atomic():
            Book.objects.create(name = book_name,published_date = published_date)

        return Response({
            'status':'success',
            'message':'Book created successfully....'
        },
        status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# create book images
@api_view(['POST'])
def create_book_images(request):
    try:
        book_id = request.data.get('book_id')
        images = request.FILES.getlist('image')
        if not book_id:
            return Response({
                'status':"failed",
                "message" : "'id' must be given"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        try:
            book_data = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
            return Response({
                'status':"failed",
                "message" : "Book not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )

        list_img = []
        if images:
            for img in images:
                save_path = default_storage.save(f'{book_data.name}/{img}',ContentFile(img.read()))
                BookImages.objects.create(image = save_path, book = book_data)
                list_img.append(default_storage.url(save_path))

        return Response({
            'status':'success',
            'message':'Book Images created successfully....'
        },
        status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
# Author create
@api_view(['POST'])
def create_author(request):
    try:
        author_name = request.data.get('name')
        book_id = request.data.get('book_id')
        country = request.data.get("country")

        if not book_id:
            return Response({
                'status':"failed",
                "message" : "'book_id' must be required"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        try:
            books = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
             return Response({
                'status':"failed",
                "message" : "Book not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        with transaction.atomic():
            Author.objects.create(name = author_name, books = books, country = country)
            return Response({
                'status':'success',
                'message':'Author created successfully....'
            },
            status=status.HTTP_201_CREATED
            )

    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# Read author(without serializer)
@api_view(['POST'])
def fetch_author(request):

    try:
        author_id = request.data.get('id')
        search = request.data.get('search')
        author = Author.objects.all()
        try:
            if author_id:
                author = Author.objects.get(id = author_id)
        except Author.DoesNotExist:
            return Response({
                "status" : "failed",
                "message" : "Author not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        if search:
            author = author.filter(Q(name__icointains = search) | Q(country__icontains = search) | Q(books__icontains = search))

        author_data = []
        for data in author:
            author_data.append({
                "id" : data.id,
                "name" : data.name,
                "book_id" : data.books.id,
                "country" : data.country
            })
        return Response({
            "status" : "success",
            "message" : "Author data fetch successfully....",
            "data" : author_data
        },
        status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 

# fetch book(without serializer)
@api_view(['POST'])
def fetch_book(request):

    try:
        book_id = request.data.get('id')
        search = request.data.get('search')

        books = Book.objects.all()
        try:
            if book_id:
                books = Book.objects.filter(id = book_id)
        except Book.DoesNotExist:
            return Response({
                    "status" : "failed",
                    "message" : "Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
        if search:
            books = books.filter(Q(name__icontains = search))

        book_data = []
        for book in books:
            book_images = []
            for img in book.images.all():
                if img.image:
                    book_images.append(img.image.url)

            book_data.append({
                "id" : book.id,
                "name" : book.name,
                "published_date" : book.published_date,
                "images" : book_images,

            })
        
        return Response({
            "status" : "success",
            "message" : "Book data fetch successfully....",
            "data" : book_data
        },
        status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# fetch book (with serializer)
@api_view(['POST'])
def fetch_book_details(request):

    try:
        book_id = request.data.get('id')
        search = request.data.get('search')
        books = Book.objects.all()
        try:
            if book_id:
                books = Book.objects.filter(id = book_id)
        except Book.DoesNotExist:
            return Response({
                    "status" : "failed",
                    "message" : "Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
        if search:
            books = books.filter(Q(name__icontains = search))
        
        serializer = BookSerializer(books,many = True)
        return Response({
                "status" : "success",
                "message" : "Book data fetch successfully....",
                "data" : serializer.data
            },
            status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
# update book
@api_view(['PUT'])
def update_book(request):

    try:
        book_id = request.data.get('id')
        book_name = request.data.get('name')
        published_date = request.data.get('date')
        images = request.FILES.getlist('image')

        if not book_id:
            return Response({
                'status':"failed",
                "message" : "'book_id' must be required"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            books = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
            return Response({
                    "status" : "failed",
                    "message" : "Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
        
        if book_name:
            books.name = book_name

        if published_date:
            books.published_date = published_date
        
        if images:
            book_images = BookImages.objects.filter(book = books)

            book_images.delete()
            for img in images:
                save_path = default_storage.save(f'{books.name}/{img}',ContentFile(img.read()))
                BookImages.objects.create(image = save_path,book = books)

        with transaction.atomic():
            books.save()

            return Response({
                "status": "success", 
                "message": "Updated successfully"
                },
                status=status.HTTP_200_OK
                )
    except Exception as e:
        return Response({
            'status':'error',
            'message' : str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


