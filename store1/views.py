from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Test, Products
from .serializers import TestSerializer, ProductSerializer

@api_view(['GET', 'POST'])
def store(request):
    
    if request.method == 'GET':

        s = Test.objects.all()
        serializer = TestSerializer(s, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def store_detail(request, pk):

    try:
        s = Test.objects.get(pk=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TestSerializer(s)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestSerializer(s, data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':

        s = Products.objects.all()
        serializer = ProductSerializer(s, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    

