from django.urls import path
from . import views

urlpatterns = [
    path('handle-request/<str:pk>/', views.handlerequest, name = "handlerequest"),
    path('initialise-payment/<int:pk>/', views.initialise_payment, name = "initialise_payment"),
]