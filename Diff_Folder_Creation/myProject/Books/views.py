from rest_framework import status
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Author,Book,BookImages
from .serializers import AuthorSerializer,BookSerializer
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.db.models import Q


# create author without serializer
@api_view(['POST'])
def create_author(request):

    try:
        author_name = request.data.get('name')
        country = request.data.get('country')

        with transaction.atomic():
            Author.objects.create(name = author_name,country = country)
            return Response({
                'status':'success',
                'message':'Author created successfully'
            },
            status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# create book
@api_view(['POST'])
def create_book(request):
    try:
        book_name = request.data.get('name')
        published_date = request.data.get('date')
        author_id = request.data.get('author_id')

        if not author_id:
            return Response({
                'status':'failed',
                'message':"'author_id' must be required"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author = Author.objects.get(id = author_id)
        except Author.DoesNotExist:
            return Response({
                'status':'failed',
                'message':"Author not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        with transaction.atomic():
            Book.objects.create(name = book_name,published_date = published_date,author = author)
            return Response({
                'status':'success',
                'message':'Book created successfully....'
            },
            status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    

    
# create images
@api_view(['POST'])
def create_book_images(request):
    try:
        book_id = request.data.get('book_id')
        images = request.FILES.getlist('image')

        if not book_id:
            return Response({
                'status':'failed',
                'message':"'book_id' must be required"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        try:
            book = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
            return Response({
                'status':'failed',
                'message':"Book not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        for img in images:
            save_path = default_storage.save(f'{book.name}/{img}',img)
            BookImages.objects.create(book = book,image = save_path)
            
        return Response({
            'status':'success',
            'message':'Book Images created successfully....'
        },
        status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# fetch author
@api_view(['POST'])
def fetch_author(request):

    try:
        author_id = request.data.get('id')
        search = request.data.get('search')
        if author_id:
            try:
                author = Author.objects.get(id = author_id)
            except Author.DoesNotExist:
                return Response({
                'status':'failed',
                'message':"Author not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )

        author = Author.objects.all()

        if search:
            author = author.filter(Q(name__icontains = search) | Q(country__icontains = search) | Q(book__icontains = search))

        author_data = []
        for data in author:
            books = []
            for book in data.books.all():
                books.append(book.id)

            author_data.append({
                'id':data.id,
                'name':data.name,
                'country':data.country,
                "books":books
            })
        return Response({
            'status':'success',
            'message':'Fetched Author data.....',
            "data":author_data
        },
        status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
# fetch book
@api_view(['POST'])
def fetch_book(request):
    try:
        book_id = request.data.get('id')
        search = request.data.get('search')
        search_date = request.data.get('search_date')

        if book_id:
            book = Book.objects.filter(id = book_id)

        book = Book.objects.all()        
        if search:
            book = book.filter(Q(name__icontains = search))

        if search_date:
            book = book.filter(published_date = search_date)

        book_data = []
        for data in book:
            images = []
            for img in data.images.all():
                images.append(img.image.url)
            book_data.append({
                'id':data.id,
                'name':data.name,
                'published_date': data.published_date,
                'images':images
            })
        return Response({
                'status':'success',
                'message':'Fetched Book data.....',
                "data":book_data
            },
            status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# fetch book (with serializer)
@api_view(['POST'])
def fetch_book_details(request):

    try:
        book_id = request.data.get('id')
        search = request.data.get('search')
        search_date = request.data.get('search_date')
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
        
        if search_date:
            books = books.filter(published_date = search_date)
        
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


# update author
@api_view(['PUT'])
def update_author(request):

    try:
        author_id = request.data.get('id')
        author_name = request.data.get('name')
        country = request.data.get('country')

        if not author_id:
            return Response({
                'status':'failed',
                'message':"'id' must be required"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author = Author.objects.get(id = author_id)
        except Author.DoesNotExist:
            return Response({
                'status':'failed',
                'message':"Author not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        if author_name:
            author.name = author_name
        if country:
            author.country = country

        with transaction.atomic():
            author.save()
            return Response({
                'status':'success',
                'message':"Author Updated ...."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response({
            'status':'error',
            'message':str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

# update book
@api_view(['PUT'])
def update_book(request):

    try:
        book_id = request.data.get('id')
        author_id = request.data.get('author_id')
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
        if author_id:
            try:
                author = Author.objects.get(id = author_id)
                books.author = author
            except Author.DoesNotExist:
                return Response({
                    'status':'failed',
                    'message':"Author not found"
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
                save_path = default_storage.save(f'{books.name}/{img}',img)
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


