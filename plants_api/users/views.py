from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets , mixins
from rest_framework.views import APIView
from .serializers import UserSerializer , ProfileSerializer , GroupSerializer , PermissionSerializer
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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile' , 'auth_token')
    serializer_class =  UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    def create(self, validated_data):

        groups = validated_data.data.pop('groups')
        permissions = validated_data.data.pop('user_permissions')
        clearPassNoHash = validated_data.data['password']

        user = User.objects.create_user(**validated_data.data)
        for group in groups:
            user.groups.add(group)

        for permission in permissions:
            user.user_permissions.add(permission)

        return JsonResponse({"result" : "user added" })

    def update(self, request, pk=None):

        if pk is not None:

            user = User.objects.filter(pk=pk).first()

            try:
                del request.data["password"]
            except:
                pass

            try:
                user.groups.clear()

                for group in request.data["groups"]:
                    user.groups.add(group)

                del request.data["groups"]
            except:
                pass

            try:
                user.permissions.clear()

                for permission in request.data["user_permissions"]:
                    user.user_permissions.add(permission)

                del request.data["user_permissions"]
            except:
                pass

            for value in request.data:
                setattr(user, value, request.data[value])

            user.save()
            return Response({"result" : UserSerializer(user).data })

        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def search_user(self, request, pk=None):
        name = self.request.query_params.get('username', None)
        result = helpers.search(self.queryset , "username__icontains" , name , UserSerializer )

        json = JSONRenderer().render(result)
        return HttpResponse(json)

    @action(methods=['get'], detail = True)
    def get_user_permissions(self , request , pk):

        user =  User.objects.filter(pk = pk).first()

        if user.is_superuser:
            permissions = Permission.objects.all().values()
        else:
            permissions = user.user_permissions.all().values() | Permission.objects.filter(group__user=user).values()

        return JsonResponse({"result" : list(permissions)})


    @action(methods=['get'], detail = True)
    def get_user_groups(self , request , pk):

        user =  User.objects.filter(pk = pk).first()
        groups = user.groups.all().values()


        return JsonResponse({"result" : list(groups)})



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
            access_token = request.COOKIES["token-access"]
            validated_token = jwt.get_validated_token(access_token)

            user = jwt.get_user(validated_token)

            retrieved_permanent_token , created = Token.objects.get_or_create(user=user)

            print(created)

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


class SignUpViewSet(mixins.CreateModelMixin , viewsets.GenericViewSet):
    http_method_names = ['post', 'head']
    queryset = User.objects.all().select_related('profile')
    serializer_class =  UserSerializer

    def create(self, validated_data):

        date_joined =  validated_data.data.pop('date_joined')
        groups = validated_data.data.pop('groups')
        permissions = validated_data.data.pop('user_permissions')


        user = User.objects.create_user(**validated_data.data)

        if date_joined is None:
            user.date_joined = datetime.now()

        user.save()

        for group in groups:
            user.groups.add(group)

        for permission in permissions:
            user.user_permissions.add(permission)

        return JsonResponse({"result" : "user added" } , status = 200)

        #except:
        #    return JsonResponse({"result" : "Bad Request" } , status = 400)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(methods=['get'], detail = True)
    def get_group_permissions(self , request , pk):

        group =  Group.objects.filter(pk = pk).first()
        group_permissions = group.permissions.all().values()


        return JsonResponse({"result" : list(group_permissions)})



class PermissionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


#class CustomObtainAuthToken(ObtainAuthToken):
#    def post(self, request, *args, **kwargs):
#        token = Token.objects.get(key=response.data['token'])
#        return Response({'token': token.key, 'id': token.user_id})

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
