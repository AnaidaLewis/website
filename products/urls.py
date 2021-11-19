from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'location', views.AddressViewSet)



urlpatterns = [
    path('', views.apiOverview, name = "apiOverview"),
    path('products/', views.products, name = "all_products"),
    path('product-create/', views.productCreate, name = "productCreate"),
    path('product-detail/<int:pk>/', views.productDetail, name = "productDetail"),
    path('product-update/<int:pk>/', views.productUpdate, name = "productUpdate"),
    path('product-delete/<int:pk>/', views.productDelete, name = "productDelete"),


    path('reviews/', views.reviews, name = "all_reviews"),
    path('review-create/<int:pk>/', views.reviewCreate, name = "reviewCreate"),
    path('review-delete/<int:pk>/', views.reviewDelete, name = "reviewDelete"),
    
    
    path('place/', include(router.urls)),
    path('create-order/', views.createOrder.as_view()),
    path('place-order/<int:pk>/', views.customerOrder.as_view()),

    path('address/<int:pk>/', views.customerAddress.as_view(), name = "createAddress"),
    
    # path('add-order-items/', views.addOrderItems, name = "addOrderItems"),
    # path('user-order/', views.UserOrder, name = "UserOrder"),


]