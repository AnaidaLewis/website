from rest_framework import serializers
from .models import Product, Review, Order, EventAddress
from register1.models import myUser

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    #Django bug, u need to define boolean fields again sometimes as it doesn't retain its default value
    availability = serializers.BooleanField(default = True)
    # used related_name in review model to relate review to product
    review = ReviewSerializer(many = True, read_only = True) 
    class Meta:
        model = Product
        fields = ['id','user','name','category','image','price','availability','description','createdAt','review']



class EventAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    location = EventAddressSerializer(many = False, read_only = True)
    class Meta:
        model = Order
        fields = '__all__'

#     def create(self, user, validated_data):
#         items = validated_data.pop('items')
#         order = Order.objects.create(user = user, **validated_data)
#         for item in items:
#             product = Product.objects.get(id = item['product'])
#             name = item['name']
#             hours = item['hours']
#             schedule = item['schedule']
#             OrderItem.objects.create(order = order, product = product, name = name, hours = hours, schedule = schedule)
#         return order

