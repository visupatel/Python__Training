from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product,ProductImages
from rest_framework import status 
from django.db import transaction
from django.db.models import Q


# post
@api_view(['POST'])
def create_prod(request):
    try:
        prod_name = request.data.get('name')
        prod_price = request.data.get('price')      
        
        with transaction.atomic():
            Product.objects.create(name = prod_name,price = prod_price)
            return Response({'status' : 'success', 'message':'prodect created successfully....'})
    except Exception as e:
        return Response({'status' : 'Error', 'message' : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# post 
@api_view(['POST'])
def create_prod_img(request):
    try:
        prod_name_id  = request.data.get('prod_id')
        try:
            if not prod_name_id:
                return Response({'status':'failed','message': 'Id not found Product not created'},status=status.HTTP_400_BAD_REQUEST)  
            prod_name = Product.objects.get(id = prod_name_id)
        
        except Product.DoesNotExist:
            return Response({'status':'failed','message':'Product Not Found'},status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('image')

        if not images:
            return Response({'status':'failed','message':'No images here'},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            img_list = []
            for img in images:
                new_img = ProductImages.objects.create(product=prod_name, image = img)
                img_list.append(new_img.image.url) 
            
            return Response({'status' : 'success', 'message':'product created successfully....'})
    except Exception as e:
        return Response({'status' : 'Error', 'message' : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# get product with images
@api_view(['POST'])
def get_img(request):
    try:
        prod_id = request.data.get('id')
        try:
            products = Product.objects.all()
            if prod_id:
                products = Product.objects.filter(id = prod_id)
        except Product.DoesNotExist:
            return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        prod_data = []
        for prod in products:
            images = []
            for img in prod.images.all():
                if img.image:
                    images.append(img.image.url)

            prod_data.append({
                "id":prod.id,
                "product":prod.name,
                "price" : prod.price,
                "image" : images
                })

        return Response({"status" : "success", "message" : "Fetch Product Images...", "products":prod_data},status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Search
@api_view(['POST'])
def search(request):
    try:
        search = request.data.get('search')
        queryset = Product.objects.all()
        
        if search:
            queryset = queryset.filter(Q(name__icontains = search) | Q(price__icontains = search) | Q(id__icontains = search))
            
        products = []
        for prod in queryset:
            images = []
            
            for img in prod.images.all():
                if img.image:
                    images.append(img.image.url)

            temp = {"id" : prod.id,"name" : prod.name,"price" : prod.price,"image" : images}
            products.append(temp)

        return Response({"status":"success","message": f"Searched {search} data:", "products":products})
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


# update product
@api_view(['PUT'])
def update_product(request):
    try:
        prod_id = request.data.get('id')
        name = request.data.get('name')
        price = request.data.get('price')
        if not prod_id:
            return Response({'status':'failed','message': 'product Id not found'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            products = Product.objects.get(id = prod_id)
        except Product.DoesNotExist:
            return Response({"status": "failed", "message": "ID not found."}, status=status.HTTP_404_NOT_FOUND)

        if name:
            products.name = name

        if price:
            products.price = price
        
        with transaction.atomic():
            products.save()
            return Response({"status" : "success","message":"Updated successfully"},status= status.HTTP_200_OK)      
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Update product images
@api_view(['PUT'])
def update_prod_images(request):
    try:
        prod_id = request.data.get('id')
        if not prod_id:
            return Response({'status':'failed','message': 'product Id not found'},status=status.HTTP_404_NOT_FOUND)
        
        prod_name_id = request.data.get('prod_id')
        if not prod_name_id:
            return Response({'status':'failed','message': 'product name Id not found'},status=status.HTTP_404_NOT_FOUND)

        try: 
            prod = Product.objects.get(id=prod_name_id)

        except Product.DoesNotExist:
            return Response({"status": "failed", "message": "Product not found."},status=status.HTTP_404_NOT_FOUND)

        try:
            product_img = ProductImages.objects.get(id=prod_id)

        except ProductImages.DoesNotExist:
            return Response({"status": "failed", "message": "ProductImages not found."},status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('image')

        if not images:
            return Response({"status": "failed", "message": "No image found"},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # single image
            if len(images) == 1:
                product_img.image = images[0]
                product_img.save()

            # multiple images
            else:
                product_img.delete()
                for img in images:
                    ProductImages.objects.create(product=prod,image=img)    
            return Response({"status": "success", "message": "Updated successfully"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error","message": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete product
@api_view(['DELETE'])
def delete_product(request):
    try:
        prod_id = request.data.get('id')
        if not prod_id:
            return Response({'status':'failed','message': 'product Id not found'},status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(id = prod_id)
        except Product.DoesNotExist:
            return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
    except Exception as e:
        return Response({"status":"Error","message" : str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)

