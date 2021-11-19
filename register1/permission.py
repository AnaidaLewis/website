from django.core.checks import messages
from rest_framework import permissions
from .models import myUser

class SuperuserPermission(permissions.BasePermission):
    message = 'only super users allowed'

    def has_permission(self,request,view):
        try:
            user = myUser.objects.get(email = request.user)
            if user.is_superuser:
                return True
            return False
        except:
            return False
        
