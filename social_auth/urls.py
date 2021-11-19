from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('google/',views.googleAuth, name = "googleAuth"), # once u signIn then go to inspect and console that is the auth_token
    #path('accounts/', include('allauth.urls')), #in this fully automated the login and all
    path('logout', LogoutView.as_view()),
]