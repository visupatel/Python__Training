from datetime import date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Author,Book,BookImages
from .seializers import AuthorSerializer,BookSerializer,BookImageSerializer
from django.core.files.storage import default_storage
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage

class AuthorView(APIView):
    def post(self,request):
        try:
            author_name = request.data.get('author_name')
            country = request.data.get('country')
            
            if not author_name :
                return Response({
                    "status":"failed",
                    "message":"'author_name' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
                
            author_names = Author.objects.filter(name = author_name)
            if len(author_names) > 0:
                return Response({
                        "status":"failed",
                        "message":f"'{author_name}' name is already exists please enter another name"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            if not country:
                return Response({
                    "status":"failed",
                    "message":"'country' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )

            if not country.isalpha():
                return Response({"status":"failed","message":"'country' must be in string"},status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                Author.objects.create(name = author_name,country = country)
                return Response({
                    'status':'success',
                    'message':'Author created successfully....'
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
        
    def get(self,request):
        try:
            author_id = request.data.get('id')
            page_number = request.data.get('page_number')
            page_size = request.data.get('page_size')
            search = request.data.get('search')

            if not page_number or not page_size:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except ValueError:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' is integers only"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            if page_number <= 0 or page_size <= 0:
                return Response({
                    "status":"failed" ,
                    "message":"'page_number' and 'page_size' must be greater than 0",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            author = Author.objects.all()

            if author_id:
                author = author.filter(id = author_id)

            if search:
                author = author.filter(Q(name__icontains = search) | Q(country__icontains = search) | Q(books__id__icontains = search) | Q(books__name__icontains = search))
            
            paginator = Paginator(author, page_size)

            try:
                author = paginator.page(page_number)
            except EmptyPage:
                return Response({
                        "status":"failed" ,
                        "message":"page not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
                    
            author_data = []
            for data in author:
                books = []
                for book in data.books.all():
                    books.append({
                        'id':book.id,
                        'name':book.name,
                    })
                author_data.append({
                    'id' : data.id,
                    'name':data.name,
                    'country':data.country,
                    'books':books
                })
            
            return Response({
                'status':'success',
                'message':'Author data fetched....',
                'current_page':page_number,
                "total_items":paginator.count,
                "total_pages":paginator.num_pages,
                'data':author_data
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
        
    def put(self,request):
        try:
            author_id = request.data.get('author_id')
            new_name = request.data.get('name')
            new_country = request.data.get('country')
            if not author_id:
                return Response({
                    'status':'failed',
                    'message':"'author_id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            try:
                author = Author.objects.get(id = author_id)
            except Author.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "Author not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )

            if new_name:
                authors = Author.objects.filter(name = new_name)
                if len(authors) > 0:
                    return Response({
                            "status":"failed",
                            "message":f" '{new_name}' name is already exists please enter another name"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                        )
                author.name = new_name

            if new_country:
                if not new_country.isalpha():
                    return Response({
                        "status":"failed",
                        "message":"'country' must be in string"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                author.country = new_country

            with transaction.atomic():
                author.save()
                return Response(
                {
                    "status": "success",
                    "message": "Author data updated...",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    
    def delete(self,request):
        try:
            author_id = request.data.get('author_id')
            if not author_id:
                return Response({
                    'status':'failed',
                    'message':"'author_id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                author = Author.objects.get(id = author_id)
            except Author.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "Author not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            author.delete()
            return Response(
                {
                    "status": "success",
                    "message": "Author data deleted....",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

class BookView(APIView):
    def post(self,request):
        try:
            book_name = request.data.get('book_name')
            author_id = request.data.get('author_id')
            published_date = request.data.get('published_date')

            if not book_name :
                return Response({
                    "status":"failed",
                    "message":"'book_name' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            if not author_id :
                return Response({
                    "status":"failed",
                    "message":"'author_id' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                author_id = int(author_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'author_id' must be in integer"
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
            
            if not published_date :
                return Response({
                    "status":"failed",
                    "message":"'published_date' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                date.strptime(published_date,'%Y-%m-%d')
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'published_date' must be in foramt(YYYY-MM-DD)"
                },
                status=status.HTTP_400_BAD_REQUEST
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
        
    def get(self,request):
        try:
            book_id = request.data.get('id')
            page_number = request.data.get('page_number')
            page_size = request.data.get('page_size')
            search = request.data.get('search')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not page_number or not page_size:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except ValueError:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' is integer only"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            if page_number <= 0 or page_size <= 0:
                return Response({
                    "status":"failed" ,
                    "message":"'page-number' and 'page_size' must be greater than 0"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            book = Book.objects.all()
            
            if book_id:
                try:
                    book_id = int(book_id)
                except ValueError:
                    return Response({
                        "status":"failed",
                        "message":"'book_id' must be in integer"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                book = book.filter(id = book_id)
            
            if search:
                book = book.filter(Q(name__icontains = search) | Q(author__name__icontains = search))
            
            if start_date and end_date:
                try:
                    date.strptime(start_date,'%Y-%m-%d')
                    date.strptime(end_date,'%Y-%m-%d')
                except ValueError:
                    return Response({
                        "status":"failed",
                        "message":"'end_date' and 'start_date' must be in foramt(YYYY-MM-DD)"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                book = book.filter(published_date__range = (start_date,end_date))

            paginator = Paginator(book,page_size)

            try:
                book = paginator.page(page_number)
            except EmptyPage:
                return Response({
                        "status":"failed" ,
                        "message":"page not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
                
            book_data = []
            for data in book:
                images = []
                for img in data.images.all():
                    images.extend(img.image)

                book_data.append({
                    'id':data.id,
                    'name':data.name,
                    'published_date': data.published_date,
                    'author':data.author.name,
                    'images':images
                })

            return Response({
                    'status':'success',
                    'message':'Fetched Book data.....',
                    "current_page": page_number,
                    "total_items": paginator.count,
                    "total_pages": paginator.num_pages,
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
        
    def put(self,request):
        try:
            book_id = request.data.get('book_id')
            new_name = request.data.get('name')
            published_date = request.data.get('date')
            author_id = request.data.get('author_id')

            if not book_id:
                return Response({
                    'status':'failed',
                    'message':"'book_id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                book = Book.objects.get(id = book_id)
            except Book.DoesNotExist:
                return Response({
                    "status":"failed",
                    "message":"Book not found",
                },
                status=status.HTTP_404_NOT_FOUND
                )

            if new_name:
                book.name = new_name
            if published_date:
                try:
                    date.strptime(published_date,'%Y-%m-%d')
                except ValueError:
                    return Response({
                        "status":"failed",
                        "message":"'published_date' must be in foramt(YYYY-MM-DD)"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                book.published_date = published_date
            if author_id:
                try:
                    author_id = int(author_id)
                except ValueError:
                    return Response({
                        "status":"failed",
                        "message":"'author_id' must be in integer"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    author_data = Author.objects.get(id = author_id)
                    book.author = author_data
                except Author.DoesNotExist:
                    return Response({
                        'status':'failed',
                        'message':'Author not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )

            with transaction.atomic():
                book.save()

                return Response(
                {
                    "status": "success",
                    "message": "Book data updated...",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    
    def delete(self,request):
        try:
            book_id = request.data.get('book_id')
            if not book_id:
                return Response({
                    'status':'failed',
                    'message':"'book_id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )

            try:
                book_id = int(book_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'book_id' must be in integer"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                book = Book.objects.get(id = book_id)
            except Book.DoesNotExist:
                return Response({
                    "status":"failed",
                    "message":"Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            book.delete()
            return Response(
                {
                    "status": "success",
                    "message": "Book data deleted....",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    
class BookImageView(APIView):
    def post(self,request):
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
                book_id = int(book_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":f"'book_id' must be in integer"
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
            
            if not images:
                return Response({
                    'status':'failed',
                    'message':"'image' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            list_images = []
            for img in images:
                save_path = default_storage.save(f'book_images/{book.name}/{img}',img)
                new_image = default_storage.url(save_path)
                list_images.append(new_image)
            BookImages.objects.create(book = book,image = list_images)
                
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
        
    def get(self,request):
        try:
            bookImages = BookImages.objects.all()
            book_data = []
            for data in bookImages:
                images = []
                for img in data.image:
                    images.append(img)
                book_data.append({
                    'id':data.id,
                    'book':data.book.name,
                    'images':images
                })
            return Response({
                'status':'success',
                'message':'Book Images Fetched....',
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
    
    def put(self,request):
        try:
            book_img_id = request.data.get('id')
            book_id = request.data.get('book_id')
            images = request.FILES.getlist('image')
            
            if not book_img_id:
                return Response({
                    'status':'failed',
                    'message':"'id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                book_img_id = int(book_img_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'id' must be in integer"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                bookImage = BookImages.objects.get(id = book_img_id)
            except BookImages.DoesNotExist: 
                return Response({
                    "status": "failed",
                    "message": "Book Image not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            if book_id:
                try:
                    book_id = int(book_id)
                except ValueError:
                    return Response({
                        "status":"failed",
                        "message":"'book_id' must be in integer"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    book = Book.objects.get(id = book_id)
                    bookImage.book = book
                except Book.DoesNotExist:
                    return Response({
                        'status':'failed',
                        'message':'Book not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
                
            if images:
                del bookImage.image
                image = []
                for img in images:
                    save_path = default_storage.save(f'book_images/{bookImage.book.name}/{img}',img)
                    new_image = default_storage.url(save_path)
                    image.append(new_image)
                bookImage.image = image

            with transaction.atomic():

                bookImage.save()
                return Response(
                {
                    "status": "success",
                    "message": "Book Image updated...",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    
    def delete(self,request):
        try:
            book_img_id = request.data.get('id')
            if not book_img_id:
                return Response({
                    'status':'failed',
                    'message':"'id' must be given"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                book_img_id = int(book_img_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'id' must be in integer"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                bookImage = BookImages.objects.get(id = book_img_id)
            except BookImages.DoesNotExist: 
                return Response({
                    "status": "failed",
                    "message": "Book Image not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            bookImage.delete()
            return Response(
                {
                    "status": "success",
                    "message": "Book images deleted....",
                },
                status=status.HTTP_200_OK,
            )
        
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    
class AuthorViewSerializer(APIView):
    def get_object(self,pk):
        author = Author.objects.filter(id = pk)
        return author
        
    def get(self,request):
        try:
            author_id = request.data.get('id')
            page_number = request.data.get('page_number')
            page_size = request.data.get('page_size')
            search = request.data.get('search')

            if not page_number or not page_size:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except ValueError:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' is integer only"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            if page_number <= 0 or page_size <= 0:
                return Response({
                    "status":"failed" ,
                    "message":"'page_number' and 'page_size' must be greater than 0"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            author = Author.objects.all()
            if author_id:
                author = self.get_object(author_id)
            
            if search:
                author = author.filter(Q(name__icontains = search) | Q(country__icontains = search) | Q(books__id__icontains = search) | Q(books__name__icontains = search))
            
            paginator = Paginator(author, page_size)

            try:
                author = paginator.page(page_number)
            except EmptyPage:
                return Response({
                        "status":"failed" ,
                        "message":"page not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
            serializer = AuthorSerializer(author,many = True)
            for data in serializer.data:
                book_data = []
                for book in data['books']:
                    book_data.append({
                        'id':book['id'],
                        'name':book['name']
                        })
                data['books'] = book_data

            return Response({
                    'status':'success',
                    'message':'Author fetched....',
                    'current_page':page_number,
                    "total_items":paginator.count,
                    "total_pages":paginator.num_pages,
                    'data':serializer.data
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

class BookViewSerializer(APIView):
    def get_object(self,pk):
        book = Book.objects.filter(id = pk)
        return book
        
    def get(self,request):
        try:
            book_id = request.data.get('id')
            page_number = request.data.get('page_number')
            page_size = request.data.get('page_size')
            search = request.data.get('search')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not page_number or not page_size:
                return Response({
                    'status':'failed',
                    'message':"'page_number' or 'page_size' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except ValueError:
                return Response({
                    'status':'failed',
                    'message':"'page_number' and 'page_size' is integer only"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            if page_number <= 0 or page_size <= 0:
                return Response({
                    "status":"failed" ,
                    "message":"page and page_size must be greater than 0"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            book = Book.objects.all()
            
            if book_id:
                book = self.get_object(book_id)
            
            if search:
                book = book.filter(Q(name__icontains = search) | Q(author__name__icontains = search))
            
            if start_date and end_date:
                book = book.filter(published_date__range = (start_date,end_date))

            paginator = Paginator(book,page_size)
            try:
                book = paginator.page(page_number)
            except EmptyPage:
                return Response({
                        "status":"failed" ,
                        "message":"page not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
            
            serializer = BookSerializer(book,many = True)
            for data in serializer.data:
                for img in data['images']:
                    images = []
                    for image in img['image']:
                        images.append(image)
                    data['images'] = images

            return Response({
                    'status':'success',
                    'message':'Book fetched....',
                    "current_page": page_number,
                    "total_items": paginator.count,
                    "total_pages": paginator.num_pages,
                    'data':serializer.data
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
    
class BookImageViewSerializer(APIView):
    def get(self,request):
        try:
            images = BookImages.objects.all()
            serializer = BookImageSerializer(images,many = True)
            return Response({
                    'status':'success',
                    'message':'Book Images fetched....',
                    'data':serializer.data
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

# for multiple post method in one class
class AuthorBookView(APIView):
    def post_author(self,request):
        try:
            author_name = request.data.get('author_name')
            country = request.data.get('country')
            
            if not author_name :
                return Response({
                    "status":"failed",
                    "message":"'author_name' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
                
            author_names = Author.objects.filter(name = author_name)
            if len(author_names) > 0:
                return Response({
                        "status":"failed",
                        "message":f"'{author_name}' name is already exists please enter another name"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            if not country:
                return Response({
                    "status":"failed",
                    "message":"'country' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )

            if not country.isalpha():
                return Response({"status":"failed","message":"'country' must be in string"},status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                Author.objects.create(name = author_name,country = country)
                return Response({
                    'status':'success',
                    'message':'Author created successfully....'
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
    
    def post_book(self,request):
        try:
            book_name = request.data.get('book_name')
            author_id = request.data.get('author_id')
            published_date = request.data.get('published_date')

            if not book_name :
                return Response({
                    "status":"failed",
                    "message":"'book_name' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            if not author_id :
                return Response({
                    "status":"failed",
                    "message":"'author_id' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                author_id = int(author_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'author_id' must be in integer"
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
            
            if not published_date :
                return Response({
                    "status":"failed",
                    "message":"'published_date' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                date.strptime(published_date,'%Y-%m-%d')
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":"'published_date' must be in foramt(YYYY-MM-DD)"
                },
                status=status.HTTP_400_BAD_REQUEST
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
          
    def post_bookImage(self,request):
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
                book_id = int(book_id)
            except ValueError:
                return Response({
                    "status":"failed",
                    "message":f"'book_id' must be in integer"
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
            
            if not images:
                return Response({
                    'status':'failed',
                    'message':"'image' must be required"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            list_images = []
            for img in images:
                save_path = default_storage.save(f'book_images/{book.name}/{img}',img)
                new_image = default_storage.url(save_path)
                list_images.append(new_image)
            BookImages.objects.create(book = book,image = list_images)
                
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
        
    def post(self,request):
        try:
            if request.data.get('author_name'):
                return self.post_author(request)
                              
            elif request.data.get('book_name'):
                return self.post_book(request)
            
            elif request.data.get('book_id'):
                return self.post_bookImage(request)
            
            else:
                return Response({
                    'status':'failed',
                    'message':'Matching field is Null or not exist'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            return Response({
                'status':'failed',
                'message':str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )