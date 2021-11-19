from django.shortcuts import render
from .models import Product,Review,Order, EventAddress
from register1.models import myUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets
from rest_framework.views import APIView

from .serializer import ProductSerializer, ReviewSerializer, OrderSerializer, EventAddressSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes(())
def apiOverview(request):
    api_urls = {
        'Register': '/api/register/', 
        'Login': '/api/login/',
        'Users': '/api/users/',
        'Products': '/products/',
        'Product-detail': '/product-detail/<int:pk>/',
        'Product-create': '/product-create/',
        'Product-update': '/product-update/<int:pk>/',
        'Product-delete': '/product-delete/<int:pk>/',

        'Reviews':'/reviews/',
        'Review-create': '/review-create/<int:pk>/',
        'Review-delete': '/review-delete/<int:pk>/',

    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes(())
def products(request):
    Products = Product.objects.all()
    serializer = ProductSerializer(Products, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def productDetail(request, pk):
    try:
	    Products = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ProductSerializer(Products, many=False)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def productCreate(request):
    product_user = Product(user = request.user)
    serializer = ProductSerializer(product_user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def productUpdate(request, pk):
    try:
	    product_update = Product.objects.get(id = pk)
    except Product.DoesNotExist:
        content = {'detail': 'Invalid id'}
        return Response(content, status = status.HTTP_404_NOT_FOUND)

     #request.user is token ka user
    if product_update.user != request.user:
        return Response({'response': 'You are do not have permission to update item'})

    if request.method == 'PUT':
        serializer = ProductSerializer(instance=product_update, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def productDelete(request, pk):
    try:
	    product_delete = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        content = {'detail': 'Invalid id'}
        return Response(content, status = status.HTTP_404_NOT_FOUND)

    if product_delete.user != request.user:
        return Response({'response': 'You are do not have permission to delete item'})

    if request.method == 'DELETE':
        product_delete.delete()
        return Response('Item succsesfully delete!')


#REVIEWS

@api_view(['GET'])
@permission_classes(())
def reviews(request):
    Reviews = Review.objects.all()
    serializer = ReviewSerializer(Reviews, many = True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reviewCreate(request, pk):
    try:
	    product = Product.objects.get(id = pk)
    except Product.DoesNotExist:
        content = {'detail': 'Invalid id'}
        return Response(content, status = status.HTTP_404_NOT_FOUND)

    review_user = Review(user = request.user, product = product)
    serializer = ReviewSerializer(review_user , data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def reviewDelete(request, pk):
    product = Product.objects.get(id = pk)
    try:
	    review_delete = Review.objects.get(user = request.user, product = product)
    except Review.DoesNotExist:
        content = {'detail': 'Invalid id', 'response': 'You are do not have permission to delete item'}
        return Response(content, status = status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        review_delete.delete()
        return Response('Item succsesfully delete!')


#for the admin to see all orders
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    """
    Model View sets automatically provide list,retrieve,create,update,partial update, delete functionalities
    Read only View sets only provides the 'read-only' actions, .list() and .retrieve()
    """

#User can view all orders and create new orders here
class createOrder(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def list(self,request):
        queryset = Order.objects.filter(user = request.user)
        serializer = OrderSerializer(queryset, many = True)
        return Response(serializer.data)
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)


#user can get individual orders,update and delete orders
class customerOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
	        Orders = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'detail':'Invalid Id'},status = status.HTTP_404_NOT_FOUND)
        try:
	        Orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion to view this order"},status = status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(Orders, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
	        Orders = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'detail':'Invalid Id'},status = status.HTTP_404_NOT_FOUND)
        try:
	        Orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion to update this order"},status = status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(instance=Orders, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
	        Orders = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'detail':'Invalid Id'},status = status.HTTP_404_NOT_FOUND)
        try:
	        Orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion to delete this order"},status = status.HTTP_404_NOT_FOUND)
        Orders.delete()
        return Response({'Response': 'Item succsesfully delete!'},status = status.HTTP_200_OK)

    
#EVENT ADDRESS ********************************************************

#for the admin to see all address
class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = EventAddress.objects.all()
    serializer_class = EventAddressSerializer

    # by this i can retrieve the address based on the id of order and not the id of the address
    def retrieve(self, request,pk):
        try:
	        order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            content = {'detail': 'Invalid id'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        try:
            add = EventAddress.objects.get(order = order)
        except EventAddress.DoesNotExist:
            return Response({'Response': "Address not created for this order"},status = status.HTTP_404_NOT_FOUND)
        serializer = EventAddressSerializer(add, many=False)
        return Response(serializer.data)


#user can get individual ADDRESS,update and delete ADDRESS
class customerAddress(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventAddressSerializer

    def get(self,request,pk):
        try:
	        order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            content = {'detail': 'Invalid id'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        try:
	        orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion to view this address"},status = status.HTTP_404_NOT_FOUND)
        try:
            add = EventAddress.objects.get(order = orders)
        except EventAddress.DoesNotExist:
            return Response({'Response': "Address not created for this order"},status = status.HTTP_404_NOT_FOUND)
        serializer = EventAddressSerializer(add, many=False)
        return Response(serializer.data)


    def post(self,request,pk):
        try:
	        order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            content = {'detail': 'Invalid id'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        try:
	        orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion add Address this order"},status = status.HTTP_404_NOT_FOUND)
        try:
            add = EventAddress.objects.get(order = orders)
        except EventAddress.DoesNotExist:
            address = EventAddress(order = orders)
            serializer = EventAddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'Response': 'Address already exists'})


    def put(self, request, pk):
        try:
	        order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            content = {'detail': 'Invalid id'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        try:
	        orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion update Address this order"},status = status.HTTP_404_NOT_FOUND)
        try:
            add = EventAddress.objects.get(order = orders)
        except EventAddress.DoesNotExist:
            return Response({'Response': "Address not created for this order"},status = status.HTTP_404_NOT_FOUND)
        serializer = EventAddressSerializer(instance = add, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
	        order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            content = {'detail': 'Invalid id'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        try:
	        orders = Order.objects.get(id=pk, user = request.user)
        except Order.DoesNotExist:
            return Response({'Response': "You do not have permisssion to delete this Address of this order"},status = status.HTTP_404_NOT_FOUND)
        try:
            add = EventAddress.objects.get(order = orders)
        except EventAddress.DoesNotExist:
            return Response({'Response': "Address not created for this order"},status = status.HTTP_404_NOT_FOUND)
        add.delete()
        return Response({'Response': 'Address succsesfully delete!'},status = status.HTTP_200_OK)




#EVENT ADDRESS


#ORDERS

# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def addOrderItems(request):
#     user = myUser.objects.get(email = request.user)
#     order = Order(user = user)
#     data = request.data
#     if len(data['items']) != 0: 
#         order_serializer = OrderSerializer(order, request.data)
#         if order_serializer.is_valid():
#             order_serializer.create(request.user, request.data)
#             order_serializer.save(user = user) # this is needed for the id and user id to be diplayed on postman
#             return Response(order_serializer.data)
#         return Response(order_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'detail':'No order Items Entered'}, status = status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def UserOrder(request):
#     try:
# 	    Orders = Order.objects.filter(user = request.user)
#     except Order.DoesNotExist:
#         return Response(status = status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializer = ViewOrderSerializer(instance = Orders, many = True)
#         return Response(serializer.data)