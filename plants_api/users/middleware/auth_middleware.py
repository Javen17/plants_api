from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
#from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            access_token = request.COOKIES["token-access"]
            refresh_token = request.COOKIES["token-refresh"]
        except:
            print("cookies not set")
            access_token = False
            refresh_token = False

        try:
            permanent_token = request.COOKIES["token-permanent"]
        except:
            print("permanent cookie not set")
            permanent_token = False

        if permanent_token:
#            token = Token.objects.get(key=permanent_token)
#            user = User.objects.get(key=token.user_id)

            request.META["HTTP_AUTHORIZATION"] = "Token " + permanent_token

            response = self.get_response(request)

        elif access_token and refresh_token:
            jwt = JWTAuthentication()

            try:
                validated_token = jwt.get_validated_token(access_token)
                user = jwt.get_user(validated_token)
            except:
                user = False
                print("invalid credentials but i need this silent so the user can still log in")
                if not "login/" in request.path : 
                    if request.COOKIES.get("warning") == "false" or  request.COOKIES.get("warning") == None:
                        response = JsonResponse({"detail" : "Your credentials are invalid, this authentication requires a login after 10 minutes of inactivity please log again, if you dont you will continue as anonymous"}, status = 401)
                        response.set_cookie("warning", "true")
                        return response

            if user:
                request.META["HTTP_AUTHORIZATION"] = "Bearer " + access_token
                response = self.get_response(request)
                refresh = RefreshToken.for_user(user)
                response.set_cookie("token-access", str(refresh.access_token))
                response.set_cookie("token-refresh", str(refresh))
                response.set_cookie("warning", "false")
            else:
                response = self.get_response(request)

        else:
            response = self.get_response(request)


        return response
