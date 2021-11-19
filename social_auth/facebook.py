import facebook
from rest_framework.response import Response

class Facebook:
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return Response("the token is either invalid or has expired")