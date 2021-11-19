from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class Product(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True)
    name           = models.CharField(max_length = 200,null = False, blank = False)
    image          = models.ImageField(null = True, blank = True)
    category       = models.CharField(max_length = 200, null = True, blank = True)
    description    = models.TextField(blank = True, null = True)
    price          = models.DecimalField(max_digits = 7, decimal_places = 2)
    availability   = models.BooleanField(default = True, db_index=True)
    createdAt      = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)

    def total_price(self):
        return float(self.price)

class Review(models.Model):
    RATING_CHOICES = [(5, 'Excellent'),(4, 'Great'),(3,'Good'),(2,'Satisfactory'),(1,'Average')]
    product        = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name= 'review', null = True)
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True)
    rating         = models.CharField(max_length = 1, choices = RATING_CHOICES)
    comment        = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.rating


class Order(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True)
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    duration       = models.DecimalField(max_digits = 7, decimal_places = 2)
    schedule       = models.DateTimeField(auto_now_add = False, blank = False)
    paymentMethod  = models.CharField(max_length = 200, null = True, blank = True)
    taxPrice       = models.DecimalField(max_digits = 7, decimal_places = 2, default = 10.00)
    totalPrice     = models.DecimalField(max_digits = 7, decimal_places = 2, blank = True)
    isPaid         = models.BooleanField(default = False)
    paidAt         = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    isDelivered    = models.BooleanField(default = False)
    deliveredAt    = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    createdAt      = models.DateTimeField(auto_now_add = True, blank = False)

    def __str__(self):
        return str(self.user)

    def saveisPaid(self, *args, **kwargs): 
        self.isPaid = True
        super(Order,self).save(*args, **kwargs)


    def save(self, *args, **kwargs): #this method added up the total price inclusive of tax and sets the totalPrice field
        print(self.product)
        product = Product.objects.get(name = self.product)
        price = product.total_price()
        self.totalPrice = self.taxPrice + price
        super(Order,self).save(*args, **kwargs)

        

# class OrderItem(models.Model):
#     product      = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order        = models.ForeignKey(Order, on_delete=models.CASCADE, blank = True)
#     name         = models.CharField(max_length = 200)
#     hours        = models.DecimalField(max_digits = 7, decimal_places = 2)
#     schedule     = models.DateTimeField(auto_now_add = False, blank = False)

#     def __str__(self):
#         return self.name


class EventAddress(models.Model):
    order         = models.OneToOneField(Order, on_delete = models.CASCADE, related_name = 'location', null = True)
    address       = models.CharField(max_length = 200, null = True, blank = True)
    city          = models.CharField(max_length = 200, null = True)
    postalCode    = models.CharField(max_length = 200, null = True)
    country       = models.CharField(max_length = 200, null = True, blank = True)
    
    def __str__(self):
        return self.city
