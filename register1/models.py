from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#for token 
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,username,email,password=None):

        if username is None:
            raise ValueError('Users should have a username')
        if email is None:
            raise ValueError('Users should have an Email')
        user = self.model(username = username, email = self.normalize_email(email))
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,username,email,password):

        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(username,self.normalize_email(email),password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using = self._db)
        return user

AUTH_PROVIDERS = {'facebook':'facebook', 'google':'google', 'twitter':'twitter', 'email':'email'}

class myUser(AbstractBaseUser, PermissionsMixin):
    username          = models.CharField(max_length = 200, unique = True, blank = False, db_index= True)
    email             = models.EmailField(max_length = 200, unique = True, db_index= True)
    first_name        = models.CharField(max_length = 200, blank = True)
    last_name         = models.CharField(max_length = 200, blank = True)
    is_admin          = models.BooleanField(default = False)
    is_active         = models.BooleanField(default =False)
    is_staff          = models.BooleanField(default = False)
    is_superuser      = models.BooleanField(default = False)
    created_at        = models.DateTimeField(blank = False,auto_now_add=True)
    update_at         = models.DateTimeField(blank = False,auto_now=True)
    auth_provider     = models.CharField(max_length = 255, blank = False, null = False, default=AUTH_PROVIDERS.get('email'))


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    # For checking permissions, to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj = None):
        return self.is_admin

    #Does this user have permisssion to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_Label):
        return True

    # def save(self, *args, **kwargs):
    #     my_user = myUser(
    #             username = self.validated_data['username'],
    #             email = self.validated_data['email']
    #         )
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']

    #     if password != password2:
    #         raise ValueError({'password': 'Passwords must match!'})
    #     my_user.set_password(password)
    #     super(myUser,self).save(*args,**kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)