from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from .serializers import UserSerializer , ProfileSerializer
from rest_framework import permissions
from plants_api.helpers import helpers
from rest_framework.decorators import action
from plants_api.users.models import Profile
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile' , 'auth_token')
    serializer_class =  UserSerializer
    permission_classes = [permissions.IsAdminUser]

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

        return JsonResponse({"results" : list(permissions)})


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

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
