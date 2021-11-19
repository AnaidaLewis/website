from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/',views.reqistration_view, name = "reqistration-view"),
    path('login/', views.login, name = "login"),
    path('users/',views.myUsers, name = "users"),
    path('user-profile/', views.getUserProfile, name = "userProfile"),
    path('user-by-id/', views.getUserById, name = "getUserById"),
    path('user-update/', views.userUpdate, name = "userUpdate"),
    path('user-delete/', views.userDelete, name = "userDelete"),

    path('email-verify/',views.verifyEmail, name = "verifyEmail"),
    # path('product-delete/<int:pk>/', views.productDelete, name = "productDelete"),
]