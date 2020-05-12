from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView , TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets , mixins
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from .serializers import UserSerializer , UserExcludeSerializer , UserSerializerWithPassword , ProfileSerializer , ProfileExcludeSerializer , GroupSerializer , PermissionSerializer
from rest_framework import permissions
from plants_api.helpers import helpers
from rest_framework.decorators import action
from plants_api.users.models import Profile
from django.contrib.auth.models import Permission , Group
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import Permission , Group
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from django.contrib.auth.hashers import make_password
from urllib.parse import parse_qs
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from . import forms
from django.http import Http404
from plants_api.common.base_classes import BaseGoogleFixClass , SearchAndPatchMixin , BasePatchClass

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

User = get_user_model()


class ProfileViewSet(BaseGoogleFixClass , SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    exclude_serializer = ProfileExcludeSerializer
    
    
class UserViewSet(BaseGoogleFixClass , SearchAndPatchMixin ,viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile' , 'auth_token')
    serializer_class =  UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    exclude_serializer = UserExcludeSerializer

    def get_permissions(self):
         return super(viewsets.ModelViewSet , self).get_permissions()

    def create(self, validated_data):

        groups = validated_data.data.pop('groups')
        permissions = validated_data.data.pop('user_permissions')
        
        valid  = validate_user(self.request, validated_data)      
        
        if valid != True:
            return valid

        try:
            user = User.objects.create_user(**validated_data.data)

            for group in groups:
                user.groups.add(group)

            for permission in permissions:
                user.user_permissions.add(permission)

        except Exception as e:
            return JsonResponse({"result": "Invalid data try again, if this issue persists contact an administrator."})

        return JsonResponse({"result" : "user added" })

    def update(self, request, partial  , pk=None):
        
        try:
            user = User.objects.filter(pk=pk).first()         
            valid  = validate_user(self.request, request , user)      

            if valid != True:
                return valid

            if hasattr(request.data, "groups"):
                if hasattr(user, "groups"):
                    user.groups.clear()  
                for group in request.data["groups"]:
                    user.groups.add(group)
            
            if hasattr(request.data, "user_permissions"):
                if hasattr(user, "user_permissions"):
                    user.user_permissions.clear()
                for permission in request.data["user_permissions"]:
                    user.user_permissions.add(permission)

            request.data.pop("groups", None)
            request.data.pop("user_permissions", None)

            for value in request.data:
                setattr(user, value, request.data[value])
                user.save()

            return Response({"result" : UserSerializer(user).data })
        except:
            JsonResponse({"result" : "Something went wrong"})


    @action(methods=['get'], detail = True)
    def get_user_permissions(self , request , pk):
        user =  User.objects.filter(pk = pk).first()
        if user.is_superuser:
            permissions = Permission.objects.all().values()
        else:
            permissions = user.user_permissions.all().values() | Permission.objects.filter(group__user=user).values()

        return JsonResponse(list(permissions), safe = False)

    @action(methods=['get'], detail = True)
    def get_user_groups(self , request , pk):

        user =  User.objects.filter(pk = pk).first()
        groups = user.groups.all().values()

        return JsonResponse(list(groups), safe = False)

    
class RestorePassword(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request , *args , **kwargs):
        form = json.loads(request.body)

        try:
            email = form["email"]

            try:
                user = User.objects.get(email  = email)
            except:
                return JsonResponse({ "result" : "That email doesn't exist in our database" } , status = 400)

            temporal = helpers.get_temporal_password(user)
            html_message = render_to_string('restore_password_mail_template.html', {'username': user.username , "link" : settings.DOMAIN_NAME + "/api/me/new_password/?code="  + temporal})   

            send_mail(
            'Restaurar Contraseña Herbario Nacional',
            'Parece que deseas restaurar tu contraseña del Herbario Nacional. Si es asi accede a este enlace: '  + settings.DOMAIN_NAME + "/api/me/new_password/?code="  + temporal,
            'from@example.com',
            [user.email],
            fail_silently=False,
            html_message = html_message
             )
            return JsonResponse( {"result" : "Check your email"} )
        except: 
            return JsonResponse({"result": "Bad Request"} , status = 400)


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        try:
            response = super(TokenObtainPairView , self).post(request, *args, **kwargs)
            response.set_cookie("token-access", response.data["access"])
            response.set_cookie("token-refresh", response.data["refresh"])
            response.data = {"result":"success"}
            return response
        except:
            return JsonResponse({"result": "Something went wrong"} , status = 401)


class GeneratePermanentTokenView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self , request , *args , **kwargs):
        jwt = JWTAuthentication()

        try:
            permanent_token = request.COOKIES["token-permanent"]
            token = Token.objects.get(key=permanent_token)
            user = User.objects.get(id=token.user_id)

            hello = f"It appears you already have a permanent Token, Hi {user}"

            return JsonResponse({"result" : hello} , status = 200)
        except:
            print("the user has no cookie or the user has a cookie that should represent the permanent token but it is invalid")

        try:
            #access_token = request.COOKIES["token-access"]    
            #validated_token = jwt.get_validated_token(access_token)
           # user = jwt.get_user(validated_token)
            retrieved_permanent_token , created = Token.objects.get_or_create(user=request.user)

            response = JsonResponse({"result" : "Success"} , status = 200)

            response.set_cookie("token-permanent", retrieved_permanent_token.key)

            return response

        except:
            return JsonResponse({"result" : "Bad Request"} , status = 400)



class RemovePermanentTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self ,  request , *args , **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()

        response = JsonResponse({"result" : "Remember me deleted"})
        response.delete_cookie("token-permanent")

        return response



class WhoAmIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request , *args , **kwargs):

        try:
            user = UserSerializer(request.user)
            return JsonResponse({"data":user.data} , status = 200)

        except:
            return JsonResponse({"status":"Bad Request"} ,  status = 400)


class ModifyMyAccount(BasePatchClass , APIView):
    model = User
    serializer_class = UserSerializerWithPassword

    def patch(self, request ,  pk = None):
        return self.update(self , request , True)
    
    def put(self , request , pk = None):
        return self.update(self , request , False)

    def update(self , request, partial  = False , pk = None):
        try :
            if self.request.user.is_anonymous:
                return JsonResponse({"result" : "You must be logged in to modify your account"} , status = 401)

            valid  = validate_user(self.request, self.request , self.request.user)   #man just use request

            if valid != True:
                return valid

            self.edit(self.request , self.request.user.id , partial)
            return JsonResponse({"result" : "Success at modification"})
        except:
            return JsonResponse({"result" : "Something went wrong"} , status = 500)


class ModifyMyProfile( ModifyMyAccount ,BasePatchClass , APIView):
    model = Profile
    serializer_class = ProfileSerializer
    queryset =  Profile.objects.all()

    def update(self , request, partial  = False , pk = None):
        try :
            if self.request.user.is_anonymous:
                return JsonResponse({"result" : "You must be logged in to modify your account"} , status = 401)
   
            profile = self.queryset.filter(user = self.request.user.id).first()

            if profile is not None:
                self.edit(self.request , profile.id , partial)
                return JsonResponse({"result" : "Success at modification"})
            else: 
                JsonResponse({"result" : "Your profile wasn't found, create one if needed"} , status = 404)
        except Exception as e:
            return JsonResponse({"result" : "Something went wrong"} , status = 500)

class MyPermissions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request, *args , **kwargs):

        user =  request.user 

        if not request.user.is_anonymous:

            if user.is_superuser:
                permissions = Permission.objects.all().values()
            else:
                permissions = user.user_permissions.all().values() | Permission.objects.filter(group__user=user).values()

            return JsonResponse(list(permissions), safe = False)
        else: 
            return JsonResponse({"status":"You need to be logged to list your account permissions"} ,  status = 400)

class SignUpViewSet(mixins.CreateModelMixin , viewsets.GenericViewSet):
    http_method_names = ['post', 'head']
    queryset = User.objects.all().select_related('profile')
    serializer_class =  UserSerializer

    def create(self, validated_data):
        try:

            if validated_data.data.get('date_joined'):
                date_joined =  validated_data.data.pop('date_joined')
            if validated_data.data.get('groups'):
                validated_data.data.pop('groups')
            if validated_data.data.get('user_permissions'):
                validated_data.data.pop('user_permissions')

            validated_data.data["is_superuser"] = False
            validated_data.data["is_staff"] = False
            
            username = validated_data.data.get('username', None)
            email = validated_data.data.get('email', None)

            invalid_username = True if User.objects.filter(username= username).exists() else False 
            invalid_email = True if User.objects.filter(email= email).exists() else False 

            valid = validate_username_and_password(invalid_username , invalid_email)     

            if valid != True:
                return valid

            user = User.objects.create_user(**validated_data.data)

            if date_joined is None:
                user.date_joined = datetime.now()

            user.save()
            return JsonResponse({"result" : "user added" } , status = 200)

        except:
            return JsonResponse({"result" : "Something went wrong" } , status = 400)

class GroupViewSet(SearchAndPatchMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
         return super(viewsets.ModelViewSet , self).get_permissions()

    @action(methods=['get'], detail = True)
    def get_group_permissions(self , request , pk):
        group =  Group.objects.filter(pk = pk).first()
        group_permissions = group.permissions.all().values()
        return JsonResponse(list(group_permissions), safe = False)

class PermissionViewSet(SearchAndPatchMixin, viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        return super(viewsets.ModelViewSet , self).get_permissions()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class NewPasswordView(FormView):
    
    template_name = "users/get_new_password.html"
    form_class = forms.NewPasswordForm
    success_url = '/api/me/updated_password/'

    def get(self, request, *args, **kwargs):
        
        try:
            params = parse_qs(request.META['QUERY_STRING'])
            user = User.objects.get(temporal_password = params["code"][0])
            return super().get(self, request, *args, **kwargs)
        except: 
             raise Http404("you've met with a terrible fate, haven't you?")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        try:
            params = parse_qs(self.request.META['QUERY_STRING'])
            user = User.objects.get(temporal_password = params["code"][0])
            user.temporal_password = None
            user.set_password(form.cleaned_data['newpassword'])
            user.save()
            return super().form_valid(form)
        except: 
             raise Http404("you've met with a terrible fate, haven't you?")


class SuccessUpdatedPassword(TemplateView):
    template_name = "users/success_updated_password.html"


def validate_user(request , validated_data , user = None):
    username = validated_data.data.get('username')
    email = validated_data.data.get('email')

    invalid_username = True if User.objects.filter(username= username).exists() else False 
    invalid_email = True if User.objects.filter(email= email).exists() else False 

    if request.method in ["PUT" , "PATCH"]:
        if username == user.username:
            invalid_username = False
        if email  == user.email:
            invalid_email = False

    if not request.user.is_superuser and validated_data.data.get('is_superuser', None) == True:
        return JsonResponse({"result" : "Forbidden you don't have the privileges for creating a super user" } , status = 403)

    if not request.user.is_staff and validated_data.data.get('is_superuser', None) == True:
        return JsonResponse({"result" : "Forbidden you don't have the privileges for creating a staff" } , status = 403)

    if invalid_username and invalid_email:
        return JsonResponse({"result" : "username and email are invalid" } , status = 400)
    if invalid_username:
         return JsonResponse({"result" : "username is invalid" } , status = 400)
    if invalid_email:
        return JsonResponse({"result" : "email is invalid" } , status = 400)
    return True