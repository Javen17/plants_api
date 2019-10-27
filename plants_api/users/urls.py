from django.urls import path
from rest_framework import routers
from django.conf.urls import url
from django.urls import include, path

from plants_api.users import views
from rest_framework.authtoken.views import obtain_auth_token



from plants_api.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    url(r'^login/', obtain_auth_token),
]
