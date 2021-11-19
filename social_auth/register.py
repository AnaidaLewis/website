from rest_framework.exceptions import AuthenticationFailed
from register1.models import myUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import os, random


#makes sure all usernames are unique
def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not myUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
    return generate_username(random_username)



def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = myUser.objects.filter(email = email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            register_user = authenticate(email = email, password ="SOCIAL_SECRET")
            return {
                'username': register_user.username, 
                'email':register_user.email, 
                'tokens': Token.objects.get(user = register_user).key
                }
        else:
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)  
    else:
        user = {
            'username': generate_username(name), 'email':email,
            }
        user = myUser.objects.create(**user) 
        user.is_active = True
        user.auth_provider = provider
        user.set_password('SOCIAL_SECRET')
        user.save()

        new_user = authenticate(email = email, password = "SOCIAL_SECRET")
        return {
            # 'username': new_user.username, 
            'email':new_user.email, 
            'tokens': Token.objects.get(user = new_user).key
            }