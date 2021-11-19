from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import myUser

from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only = True)
    class Meta:
        model = myUser
        fields = ["username","email","password","password2"]
        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def save(self):
        my_user = myUser(
            username = self.validated_data['username'],
            email = self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        my_user.set_password(password)
        my_user.save()
        return my_user


class myUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default = True)
    class Meta:
        model = myUser
        exclude = ['password']
    # def update(self, instance):
    #     print(self)
    #     instance.username = self.validated_data.get('username',instance.username)
    #     instance.email = self.validated_data.get('email',instance.email)
    #     instance.password = self.validated_data.get('password',instance.password)
    #     instance.first_name = self.validated_data.get('first_name',instance.first_name)
    #     instance.last_name = self.validated_data.get('last_name',instance.last_name)
    #     instance.save()
    #     return instance



class loginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = myUser.objects.get(email=obj['email'])
        return {'token': Token.objects.get(user = user).key }

    class Meta:
        model = myUser
        fields = ['email', 'password', 'username', 'tokens']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)

        filtered_user_by_email = myUser.objects.filter(email = email)

        if filtered_user_by_email.exists():
            if filtered_user_by_email[0].auth_provider != 'email':
                raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {'email': user.email,'username': user.username}
# still the lastlogin is not gettting updated


# class loginUserSerializer(serializers.Serializer):
#     email    = serializers.EmailField(max_length = 100)
#     password = serializers.CharField(max_length = 100)
#     username = serializers.CharField(read_only = True)
#     token    = serializers.CharField(read_only = True)
#     # class Meta:
#     #     model = myUser
#     #     fields = ['email','password','username','token']
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
        
#         user = myUser.objects.get(email = email, password = password)
#         if not user.is_active:
#             raise AuthenticationFailed('Account disabled, activation link sent on email')
#         if not user:
#             raise AuthenticationFailed('Invalid credentials')
#         return {
#             'email' : user.email,
#             'username' : user.username,
#             'token': Token.objects.get(user = user).key
#         }

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 100)
    class Meta:
        model = myUser
        fields = ['token']


