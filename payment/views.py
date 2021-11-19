from django.shortcuts import render, redirect
import os
from products.models import Order, EventAddress
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from products.serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from . import Checksum

import environ

env = environ.Env()
environ.Env.read_env()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def initialise_payment(request, pk):
    try:
	    order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({'detail':'Invalid Id'},status = status.HTTP_404_NOT_FOUND)
    try:
        order = Order.objects.get(id=pk, user = request.user)
    except Order.DoesNotExist:
        return Response({'Response': "You do not have permisssion to view this order"},status = status.HTTP_404_NOT_FOUND)
    try:
        add = EventAddress.objects.get(order = order)
    except EventAddress.DoesNotExist:
        return Response({'Response': "Address not created for this order", "Create Address": 'http://127.0.0.1:8000/address/<order-id>/'},status = status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order, many=False)
    print(order.id)
    print(serializer.data)
    print(request.user)
    order_id = Checksum.__id_generator__()
    param_dict = {
        'MID': 'MERCHANT_ID',
        'ORDER_ID': order_id,
        'TXN_AMOUNT': str(serializer.data['totalPrice']),
        'CUST_ID': str(serializer.data['user']),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/payment/handle-request/' + str(order.id) + '/',
        # CAllback_url is where paytm will send a post request to confirm payment
    }
    #this creates a new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,'MERCHANT_KEY')
    return render(request, 'paytm/checkout.html', {'param_dict':param_dict})
 

# Create your views here.
@csrf_exempt
# @api_view(['POST'])
def handlerequest(request, pk):
    #paytm will send a post request here
    order = Order.objects.get(id = pk)
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    print(response_dict)
    verify = Checksum.verify_checksum(response_dict, 'MERCHANT_KEY', checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order.isPaid = True
            order.saveisPaid()
            #the 01 code is a paytm code for successful transaction
            print('order successful')
        else:
            print('order was unsuccessful because ' + response_dict['RESPMSG'])
        return render(request, 'paytm/paymentstatus.html',{'response':response_dict})